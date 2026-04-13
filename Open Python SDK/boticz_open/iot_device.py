from dataclasses import asdict

from .client import Client
from .response import GetLatestDeviceDataResponse, LatestDeviceDataRecord
from .validator import require_value


class IotDeviceService:
    def __init__(self, client: Client):
        self._client = client

    def get_latest_device_data(self, request):
        require_value(request.product_name, "product_name")
        require_value(request.device_id, "device_id")
        require_value(request.topic_name, "topic_name")
        data = self._client.request(
            "GET",
            "/iot/device/data",
            params={
                "product_name": request.product_name,
                "device_id": request.device_id,
                "topic_name": request.topic_name,
            },
        )
        return self._parse_latest_response(data)

    def send_device_command(self, request):
        require_value(request.command, "command")
        require_value(request.parameter, "parameter")
        require_value(request.device_id, "device_id")
        require_value(request.product_name, "product_name")
        require_value(request.topic_name, "topic_name")
        self._client.request("POST", "/iot/device/command", data=asdict(request))

    def bind_device(self, request):
        require_value(request.device_id, "device_id")
        self._client.request("POST", "/iot/device/bind", data=asdict(request))

    def setting(self, request):
        require_value(request.device_id, "device_id")
        require_value(request.temperature, "temperature")
        require_value(request.humidity, "humidity")
        self._client.request("POST", "/iot/device/setting", data=asdict(request))

    @staticmethod
    def _parse_latest_response(data):
        if data is None:
            return None
        record = data.get("record")
        parsed_record = None
        if record:
            parsed_record = LatestDeviceDataRecord(
                raw_topic_name=record.get("raw_topic_name"),
                payload=record.get("payload"),
                url=record.get("url"),
                created_at=record.get("created_at"),
            )
        return GetLatestDeviceDataResponse(
            product_name=data.get("product_name"),
            device_id=data.get("device_id"),
            topic_name=data.get("topic_name"),
            record=parsed_record,
        )
