"""单元测试：IotDeviceService.get_device_info"""
import json
from unittest import mock

from masrobo_rcs_sdk import APIError
from masrobo_rcs_sdk.iot_device import IotDeviceService
from masrobo_rcs_sdk.request import DeviceInfoRequest
from masrobo_rcs_sdk.config import Config
from masrobo_rcs_sdk.client import Client


class TestGetDeviceInfo:
    """测试 get_device_info 接口"""

    def _create_service(self):
        """创建带 mock session 的 IotDeviceService"""
        cfg = Config(base_url="https://api.example.com", app_id="test-app", app_key="test-key")
        client = Client(cfg)
        client.session = mock.Mock()
        return IotDeviceService(client), client

    @staticmethod
    def _make_response(status_code: int, code: int, data, msg: str = "success"):
        body = {"code": code, "msg": msg, "data": data}
        resp = mock.Mock()
        resp.status_code = status_code
        resp.text = json.dumps(body)
        resp.json.return_value = body
        return resp

    def test_success(self):
        """成功获取设备信息"""
        svc, client = self._create_service()

        fake_data = {
            "device_id": "test-device-001",
            "product_name": "AibbyPet",
            "device_name": "测试设备",
            "status": 1,
            "services": {"webrtc": {"enabled": True}},
        }
        client.session.request.return_value = self._make_response(200, code=200, data=fake_data)

        request = DeviceInfoRequest(device_id="test-device-001")
        result = svc.get_device_info(request)

        assert result is not None
        assert result["device_id"] == "test-device-001"
        assert result["product_name"] == "AibbyPet"
        assert result["services"]["webrtc"]["enabled"] is True

        # 验证请求参数
        call_args = client.session.request.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"].endswith("/iot/device/info")
        assert call_args[1]["json"]["device_id"] == "test-device-001"

    def test_success_full_fields(self):
        """成功获取设备信息（含完整字段）"""
        svc, client = self._create_service()

        fake_data = {
            "id": 42,
            "device_id": "device-full-001",
            "iot_product_id": 15,
            "product_name": "SmartSensor",
            "category_code": "sensor",
            "user_id": 888,
            "device_name": "温湿度传感器 #1",
            "active_type": ["MANUAL", "API"],
            "status": 1,
            "active_time": "2025-06-01T10:30:00",
            "deactive_time": None,
            "application_id": 300,
            "developer_id": 50,
            "app_id": "my-app",
            "application_name": "我的应用",
            "developer_name": "开发者",
            "product_title": "智能传感器 Pro",
            "device_data": {"temperature": 25.5, "humidity": 60},
            "device_data_time": "2025-06-03T12:00:00",
            "screenshot": "https://cdn.example.com/snap.jpg",
            "screenshot_time": "2025-06-03T12:00:00",
            "services": {
                "webrtc": {"enabled": False},
                "ota": {"enabled": True, "version": "2.0.1"},
            },
            "rel_role": 0,
            "rel_source": "shared",
        }
        client.session.request.return_value = self._make_response(200, code=200, data=fake_data)

        request = DeviceInfoRequest(device_id="device-full-001")
        result = svc.get_device_info(request)

        assert result["device_id"] == "device-full-001"
        assert result["product_name"] == "SmartSensor"
        assert result["device_name"] == "温湿度传感器 #1"
        assert result["device_data"]["temperature"] == 25.5
        assert result["services"]["ota"]["version"] == "2.0.1"

    def test_empty_device_id(self):
        """device_id 为空时应抛出异常"""
        svc, _ = self._create_service()
        request = DeviceInfoRequest(device_id="")
        try:
            svc.get_device_info(request)
            assert False, "应该抛出异常"
        except ValueError as e:
            assert "device_id" in str(e).lower() or "device_id" in str(e)

    def test_none_device_id(self):
        """device_id 为 None 时应抛出异常"""
        svc, _ = self._create_service()
        request = DeviceInfoRequest(device_id=None)
        try:
            svc.get_device_info(request)
            assert False, "应该抛出异常"
        except ValueError as e:
            assert "device_id" in str(e).lower() or "device_id" in str(e)

    def test_api_error_response(self):
        """API 返回业务错误时应抛出 APIError（code ≠ 200）"""
        svc, client = self._create_service()
        client.session.request.return_value = self._make_response(
            200, code=40001, data=None, msg="device not found"
        )

        request = DeviceInfoRequest(device_id="nonexistent-device")
        try:
            svc.get_device_info(request)
            assert False, "应该抛出 APIError"
        except APIError as e:
            assert e.code == 40001
            assert "device not found" in str(e)

    def test_http_error_response(self):
        """HTTP 返回 401 时应抛出 APIError"""
        svc, client = self._create_service()
        client.session.request.return_value = self._make_response(
            401, code=40100, data=None, msg="unauthorized"
        )

        request = DeviceInfoRequest(device_id="test-device")
        try:
            svc.get_device_info(request)
            assert False, "应该抛出 APIError"
        except APIError as e:
            assert e.status_code == 401
            assert e.code == 40100