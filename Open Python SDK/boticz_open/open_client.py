from .client import Client
from .config import Config
from .iot_device import IotDeviceService


class OpenClient:
    def __init__(self, base_url: str, token: str, session=None):
        client = Client(Config(base_url=base_url, token=token, session=session))
        self.IotDevice = IotDeviceService(client)

