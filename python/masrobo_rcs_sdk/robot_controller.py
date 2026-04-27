from .client import Client
from .config import Config
from .iot_device import IotDeviceService

class RobotController:
    def __init__(self, base_url: str, app_id: str, app_key: str, session=None):
        client = Client(Config(base_url=base_url, app_id=app_id, app_key=app_key, session=session))
        self.IotDevice = IotDeviceService(client)

