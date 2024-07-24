from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas


REQUEST_TIMESTAMP_FIELD_NAME = "request_timestamp"


@dataclass
class RealtimeContext:
    request_timestamp: Optional[datetime] = None

    def to_pandas(self) -> pandas.DataFrame:
        return pandas.DataFrame({REQUEST_TIMESTAMP_FIELD_NAME: [self.request_timestamp]})
