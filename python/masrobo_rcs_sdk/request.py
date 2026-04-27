from dataclasses import dataclass

TopicDeviceData = "device_data"
TopicScreenshot = "screenshot"
TopicRemoteControl = "remote_control"


@dataclass
class GetLatestDeviceDataRequest:
    product_name: str
    device_id: str
    topic_name: str


@dataclass
class SendDeviceCommandRequest:
    command: str
    parameter: str
    device_id: str
    product_name: str
    topic_name: str


@dataclass
class BindDeviceRequest:
    device_id: str


@dataclass
class TemperatureSetting:
    max_value: float
    min_value: float
    calibration: float


@dataclass
class HumiditySetting:
    max_value: float
    min_value: float
    calibration: float


@dataclass
class DeviceSettingRequest:
    device_id: str  # Device ID
    settings: str  # JSON string of settings, e.g. {"temperature":{"max_value":30,"min_value":10,"calibration":0},"humidity":{"max_value":80,"min_value":20,"calibration":0},"data_recording_interval":5,"reporting_interval":10,"alert_interval":15,"alert_battery":10}