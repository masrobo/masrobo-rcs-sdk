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
    device_id: str
    temperature: TemperatureSetting
    humidity: HumiditySetting
    data_recording_interval: int
    reporting_interval: int

