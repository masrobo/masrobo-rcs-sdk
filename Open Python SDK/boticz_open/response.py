from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class LatestDeviceDataRecord:
    raw_topic_name: str
    payload: Any = None
    url: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class GetLatestDeviceDataResponse:
    product_name: str
    device_id: str
    topic_name: str
    record: Optional[LatestDeviceDataRecord] = None

