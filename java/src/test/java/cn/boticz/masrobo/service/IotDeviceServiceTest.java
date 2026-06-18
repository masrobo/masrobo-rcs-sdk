package cn.boticz.masrobo.service;

import cn.boticz.masrobo.RobotController;
import cn.boticz.masrobo.client.Config;
import cn.boticz.masrobo.request.AddDeviceRequest;
import cn.boticz.masrobo.request.DeviceInfoRequest;
import cn.boticz.masrobo.response.DeviceQRCodeInfo;
import cn.boticz.masrobo.response.IotDeviceInfo;
import io.github.cdimascio.dotenv.Dotenv;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 集成测试：IotDeviceService.getDeviceInfo（真实 API 调用）
 * 参考 Python SDK 单元测试 {@code python/tests/test_device_info.py} 的做法
 */
class IotDeviceServiceTest {

    private static IotDeviceService service;
    private static String deviceId;
    private static String productName;

    @BeforeAll
    static void setUp() {
        // 从 java/.env 文件加载环境变量（类似 Python: load_dotenv()）
        Dotenv dotenv = Dotenv.configure()
                .directory(".")
                .filename(".env")
                .load();

        String baseUrl = dotenv.get("BASE_URL");
        String appId = dotenv.get("APP_ID");
        String appKey = dotenv.get("APP_KEY");
        deviceId = dotenv.get("DEVICE_ID");
        productName = dotenv.get("PROJECT_NAME");

        assertNotNull(baseUrl, "BASE_URL 不能为空");
        assertNotNull(appId, "APP_ID 不能为空");
        assertNotNull(appKey, "APP_KEY 不能为空");
        assertNotNull(deviceId, "DEVICE_ID 不能为空");

        // 使用 RobotController 创建客户端（类似 Python: RobotController(base_url, app_id, app_key)）
        Config config = new Config(baseUrl, appId, appKey);
        RobotController controller = new RobotController(config);
        service = controller.getIotDevice();
    }

    @Test
    void testGetDeviceInfo() {
        // 参考 Python: client.IotDevice.get_device_info(DeviceInfoRequest(device_id=DEVICE_ID))
        DeviceInfoRequest request = new DeviceInfoRequest(deviceId);
        IotDeviceInfo result = service.getDeviceInfo(request);

        System.out.println("Device info result: " + result);

        assertNotNull(result);
        assertEquals(deviceId, result.getDeviceId());
        assertEquals(productName, result.getProductName());
        assertNotNull(result.getDeviceName());
        assertTrue(result.getStatus() >= 0);

        System.out.println("设备名称: " + result.getDeviceName());
        System.out.println("产品名称: " + result.getProductName());
        System.out.println("设备状态: " + result.getStatus());
    }

    @Test
    void testAddDevice() {
        // 参考 Python: client.IotDevice.add_device(AddDeviceRequest(project_name=PRODUCT_NAME, device_id=DEVICE_ID))
        AddDeviceRequest request = new AddDeviceRequest(productName, deviceId);
        DeviceQRCodeInfo result = service.addDevice(request);
        assertNotNull(result);
        assertNotNull(result.getQrcodeUrl());
        System.out.println("addDevice 调用成功: qrcode_url=" + result.getQrcodeUrl());
    }
}