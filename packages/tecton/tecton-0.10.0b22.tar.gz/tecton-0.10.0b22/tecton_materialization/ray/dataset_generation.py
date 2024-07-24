from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional
from typing import Union

import attrs
import boto3
import pandas
import pendulum

from tecton_core import conf
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_processing_utils import split_spine
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.query import builder
from tecton_core.query import nodes
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import StagingNode
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.query_consts import valid_to
from tecton_materialization.common.task_params import get_features_params_from_task_params
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.nodes import TimeSpec
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


def run_dataset_generation(
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    # retrieve current region
    conf.set("CLUSTER_REGION", boto3.Session().region_name)

    assert materialization_task_params.dataset_generation_task_info.HasField("dataset_generation_parameters")
    dataset_generation_params = materialization_task_params.dataset_generation_task_info.dataset_generation_parameters
    params = get_features_params_from_task_params(materialization_task_params, compute_mode=ComputeMode.RIFT)

    qts = get_features_from_params(params)

    store_params = OfflineStoreParams(
        feature_view_id=params.fco.id,
        feature_view_name=params.fco.name,
        schema=dataset_generation_params.expected_schema,
        time_spec=None,
        feature_store_format_version=None,
        batch_schedule=None,
    )

    table = get_delta_writer(
        materialization_task_params,
        store_params=store_params,
        table_uri=dataset_generation_params.result_path,
        join_keys=params.join_keys,
    )
    for qt in qts:
        reader = executor.exec_qt(qt).result_table
        table.write(reader)
    table.commit()


def get_features_from_params(
    params: Union[GetFeaturesInRangeParams, GetFeaturesForEventsParams],
) -> List[NodeRef]:
    if isinstance(params, GetFeaturesForEventsParams):
        if isinstance(params.fco, specs.FeatureServiceSpec):
            return get_features_for_events_for_feature_service_qt(
                feature_set_config=params.feature_set_config,
                spine=params.events,
                timestamp_key=params.timestamp_key,
                from_source=params.from_source,
            )
        elif isinstance(params.fco, FeatureDefinitionWrapper):
            qts = get_features_for_events_qt(
                feature_definition=params.fco,
                spine=params.events,
                timestamp_key=params.timestamp_key,
                from_source=params.from_source,
            )
            return qts
    elif isinstance(params, GetFeaturesInRangeParams):
        qt = get_features_in_range_qt(
            feature_definition=params.fco,
            start_time=params.start_time,
            end_time=params.end_time,
            max_lookback=params.max_lookback,
            entities=params.entities,
            from_source=params.from_source,
        )
        return [qt]
    else:
        error = f"Unsupported params type: {type(params)}"
        raise ValueError(error)


def get_features_in_range_qt(
    feature_definition: FeatureDefinitionWrapper,
    start_time: Union[pendulum.DateTime, datetime],
    end_time: Union[pendulum.DateTime, datetime],
    max_lookback: Optional[timedelta],
    entities: Optional[Union[pandas.DataFrame]],
    from_source: Optional[bool],
) -> NodeRef:
    start_time = pendulum.instance(start_time)
    if feature_definition.feature_start_timestamp is not None:
        start_time = max(start_time, feature_definition.feature_start_timestamp)
    query_time_range = pendulum.Period(start_time, pendulum.instance(end_time))

    if feature_definition.is_temporal or feature_definition.is_feature_table:
        lookback_time_range = time_utils.temporal_fv_get_feature_data_time_limits(
            feature_definition, query_time_range, max_lookback
        )
        qt = builder.build_temporal_time_range_validity_query(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            fd=feature_definition,
            from_source=from_source,
            query_time_range=query_time_range,
            lookback_time_range=lookback_time_range,
            entities=entities,
        )
    else:
        feature_data_time_limits = time_utils.get_feature_data_time_limits(
            fd=feature_definition,
            spine_time_limits=query_time_range,
        )
        qt = builder.build_aggregated_time_range_validity_query(
            Dialect.DUCKDB,
            ComputeMode.RIFT,
            feature_definition,
            feature_data_time_limits=feature_data_time_limits,
            query_time_range=query_time_range,
            from_source=from_source,
            entities=entities,
        )

    return _add_partition_column(qt, valid_to())


def get_features_for_events_for_feature_service_qt(
    feature_set_config: FeatureSetConfig,
    spine: pandas.DataFrame,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> List[NodeRef]:
    qts = []
    if conf.get_bool("DUCKDB_ENABLE_SPINE_SPLIT"):
        spine_split = split_spine(spine, feature_set_config.join_keys)
        for spine_chunk in spine_split:
            qt = _get_historical_features_for_feature_set(feature_set_config, spine_chunk, timestamp_key, from_source)
            qts.append(qt)
    else:
        qt = _get_historical_features_for_feature_set(feature_set_config, spine, timestamp_key, from_source)
        qts.append(qt)

    return qts


def get_features_for_events_qt(
    feature_definition: FeatureDefinitionWrapper,
    spine: pandas.DataFrame,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> List[NodeRef]:
    qts = []
    if conf.get_bool("DUCKDB_ENABLE_SPINE_SPLIT"):
        spine_split = split_spine(spine, feature_definition.join_keys)
        for spine_chunk in spine_split:
            qt = _point_in_time_get_historical_features_for_feature_definition(
                feature_definition, spine_chunk, timestamp_key, from_source
            )
            qts.append(qt)
    else:
        qt = _point_in_time_get_historical_features_for_feature_definition(
            feature_definition, spine, timestamp_key, from_source
        )
        qts.append(qt)

    return [_add_partition_column(qt, timestamp_key) for qt in qts]


def _point_in_time_get_historical_features_for_feature_definition(
    feature_definition: FeatureDefinitionWrapper,
    spine: pandas.DataFrame,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> NodeRef:
    dac = FeatureDefinitionAndJoinConfig.from_feature_definition(feature_definition)
    user_data_node_metadata = {}
    user_data_node = nodes.UserSpecifiedDataNode(
        Dialect.DUCKDB, ComputeMode.RIFT, nodes.PandasDataframeWrapper(spine), user_data_node_metadata
    )

    if timestamp_key:
        user_data_node_metadata["timestamp_key"] = timestamp_key
        user_data_node = nodes.ConvertTimestampToUTCNode(
            Dialect.DUCKDB, ComputeMode.RIFT, user_data_node.as_ref(), timestamp_key
        )

    qt = builder.build_spine_join_querytree(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        dac=dac,
        spine_node=user_data_node.as_ref(),
        spine_time_field=timestamp_key,
        from_source=from_source,
        use_namespace_feature_prefix=True,
    )

    return qt


def _get_historical_features_for_feature_set(
    feature_set_config: FeatureSetConfig,
    spine: pandas.DataFrame,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
) -> NodeRef:
    user_data_node = nodes.UserSpecifiedDataNode(
        Dialect.DUCKDB, ComputeMode.RIFT, nodes.PandasDataframeWrapper(spine), {"timestamp_key": timestamp_key}
    )
    user_data_node = nodes.ConvertTimestampToUTCNode(
        Dialect.DUCKDB, ComputeMode.RIFT, user_data_node.as_ref(), timestamp_key
    )

    tree = builder.build_feature_set_config_querytree(
        Dialect.DUCKDB,
        ComputeMode.RIFT,
        feature_set_config,
        user_data_node.as_ref(),
        timestamp_key,
        from_source,
    )
    return _add_partition_column(tree, timestamp_key)


def _add_partition_column(qt: NodeRef, time_column) -> NodeRef:
    """
    Injects AddTimePartitionNode either before StagingNode(step=AGGREGATION) or at the top of the tree.
    The aim is to run this node before ODFV (if it is present) to make it part of DuckDB query.
    """

    def create_node(input_node: NodeRef) -> NodeRef:
        return AddTimePartitionNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=input_node,
            time_spec=TimeSpec(
                timestamp_key=time_column,
                time_column=time_column,
                partition_size=timedelta(days=1),
                partition_is_anchor=False,
            ),
        ).as_ref()

    def inject(tree: NodeRef) -> bool:
        """
        Traverse over the tree and return True if AddTimePartitionNode was injected before StagingNode(step=AGGREGATION)
        """
        injected = False

        if isinstance(tree.node, StagingNode) and QueryTreeStep.AGGREGATION == tree.node.query_tree_step:
            prev_input = tree.node.input_node
            new_input = create_node(prev_input)
            tree.node = attrs.evolve(tree.node, input_node=new_input)
            injected = True

        return injected or any(inject(tree=i) for i in tree.inputs)

    if inject(qt):
        return qt

    # add node at the top
    return create_node(qt)
