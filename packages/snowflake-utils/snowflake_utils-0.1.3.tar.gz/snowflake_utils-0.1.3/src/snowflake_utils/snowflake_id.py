from dataclasses import dataclass
from time import time
from typing import Optional
from datetime import datetime, timedelta, tzinfo

from .types import MAX_TS, MAX_NODE_ID, MAX_SEQUENCE


@dataclass(frozen=True)
class SnowflakeId:
    """Snowflake ID data object"""

    timestamp: int
    node_id: int
    epoch: int = 0
    sequence: int = 0

    def __post_init__(self):
        if self.epoch < 0:
            raise ValueError("epoch must not be negative!")

        if self.timestamp < 0 or self.timestamp > MAX_TS:
            raise ValueError(
                f"timestamp must not be negative and must be less than {MAX_TS}!"
            )

        if self.node_id < 0 or self.node_id > MAX_NODE_ID:
            raise ValueError(
                f"node_id must not be negative and must be less than {MAX_NODE_ID}!"
            )

        if self.sequence < 0 or self.sequence > MAX_SEQUENCE:
            raise ValueError(
                f"seq must not be negative and must be less than {MAX_SEQUENCE}!"
            )

    @classmethod
    def parse(cls, snowflake_id: int, epoch: int = 0) -> "SnowflakeId":
        return cls(
            epoch=epoch,
            timestamp=snowflake_id >> 22,
            node_id=snowflake_id >> 12 & MAX_NODE_ID,
            sequence=snowflake_id & MAX_SEQUENCE,
        )

    @property
    def milliseconds(self) -> int:
        return self.timestamp + self.epoch

    @property
    def seconds(self) -> float:
        return self.milliseconds / 1000

    @property
    def datetime(self) -> datetime:
        return datetime.utcfromtimestamp(self.seconds)

    def datetime_tz(self, tz: Optional[tzinfo] = None) -> datetime:
        return datetime.fromtimestamp(self.seconds, tz=tz)

    @property
    def timedelta(self) -> timedelta:
        return timedelta(milliseconds=self.epoch)

    @property
    def value(self) -> int:
        return self.timestamp << 22 | self.node_id << 12 | self.sequence

    def __int__(self) -> int:
        return self.value
