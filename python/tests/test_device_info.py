"""集成测试：IotDeviceService.get_device_info（真实 API 调用）"""
import os
import sys
import logging
from dotenv import load_dotenv

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from masrobo_rcs_sdk import RobotController
from masrobo_rcs_sdk.request import DeviceInfoRequest

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从 .env 文件加载环境变量
load_dotenv()

# 从环境变量读取配置
BASE_URL = os.environ.get('BASE_URL')
APP_ID = os.environ.get('APP_ID')
APP_KEY = os.environ.get('APP_KEY')
DEVICE_ID = os.environ.get('DEVICE_ID')
PRODUCT_NAME = os.environ.get('PROJECT_NAME')


class TestGetDeviceInfo:
    """使用真实环境变量调用 get_device_info API"""

    def _create_service(self):
        """使用 RobotController 创建客户端"""
        client = RobotController(
            base_url=BASE_URL,
            app_id=APP_ID,
            app_key=APP_KEY,
        )
        return client

    def test_get_device_info(self):
        """获取设备信息，验证返回的关键字段"""
        client = self._create_service()
        request = DeviceInfoRequest(device_id=DEVICE_ID)
        result = client.IotDevice.get_device_info(request)

        logger.info(f"Device info result: {result}")

        assert result is not None
        assert result["device_id"] == DEVICE_ID
        assert result["product_name"] == PRODUCT_NAME
        assert "device_name" in result
        assert "status" in result

        logger.info(f"设备名称: {result.get('device_name')}")
        logger.info(f"产品名称: {result.get('product_name')}")
        logger.info(f"设备状态: {result.get('status')}")


if __name__ == "__main__":
    """直接运行此脚本进行集成测试"""
    import pytest
    pytest.main([__file__, "-v"])