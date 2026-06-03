package cn.boticz.masrobo.service;

import cn.boticz.masrobo.client.OpenHttpClient;
import cn.boticz.masrobo.request.DeviceInfoRequest;
import cn.boticz.masrobo.response.IotDeviceInfo;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.LinkedHashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class IotDeviceServiceTest {

    @Mock
    private OpenHttpClient httpClient;

    private IotDeviceService service;

    @BeforeEach
    void setUp() {
        service = new IotDeviceService(httpClient);
    }

    @Test
    void testGetDeviceInfo_Success() {
        // Arrange
        IotDeviceInfo fakeInfo = new IotDeviceInfo();
        fakeInfo.setDeviceId("test-device-001");
        fakeInfo.setProductName("AibbyPet");
        fakeInfo.setDeviceName("测试设备");
        fakeInfo.setStatus(1);

        Map<String, Object> services = new LinkedHashMap<>();
        Map<String, Object> webrtc = new LinkedHashMap<>();
        webrtc.put("enabled", true);
        services.put("webrtc", webrtc);
        fakeInfo.setServices(services);

        when(httpClient.post(eq("/iot/device/info"), any(DeviceInfoRequest.class), eq(IotDeviceInfo.class)))
                .thenReturn(fakeInfo);

        // Act
        DeviceInfoRequest request = new DeviceInfoRequest("test-device-001");
        IotDeviceInfo result = service.getDeviceInfo(request);

        // Assert
        assertNotNull(result);
        assertEquals("test-device-001", result.getDeviceId());
        assertEquals("AibbyPet", result.getProductName());
        assertEquals("测试设备", result.getDeviceName());
        assertEquals(1, result.getStatus());
        assertTrue((Boolean) result.getServices().get("webrtc").get("enabled"));

        // 验证请求参数
        verify(httpClient).post(eq("/iot/device/info"), any(DeviceInfoRequest.class), eq(IotDeviceInfo.class));
    }

    @Test
    void testGetDeviceInfo_FullFields() {
        // Arrange
        IotDeviceInfo fakeInfo = new IotDeviceInfo();
        fakeInfo.setId(42L);
        fakeInfo.setDeviceId("device-full-001");
        fakeInfo.setIotProductId(15L);
        fakeInfo.setProductName("SmartSensor");
        fakeInfo.setCategoryCode("sensor");
        fakeInfo.setUserId(888L);
        fakeInfo.setDeviceName("温湿度传感器 #1");
        fakeInfo.setActiveType(new String[]{"MANUAL", "API"});
        fakeInfo.setStatus(1);

        Map<String, Object> deviceData = new LinkedHashMap<>();
        deviceData.put("temperature", 25.5);
        deviceData.put("humidity", 60);
        fakeInfo.setDeviceData(deviceData);

        Map<String, Object> services = new LinkedHashMap<>();
        Map<String, Object> ota = new LinkedHashMap<>();
        ota.put("enabled", true);
        ota.put("version", "2.0.1");
        services.put("ota", ota);
        fakeInfo.setServices(services);

        fakeInfo.setRelRole(0);
        fakeInfo.setRelSource("shared");

        when(httpClient.post(eq("/iot/device/info"), any(DeviceInfoRequest.class), eq(IotDeviceInfo.class)))
                .thenReturn(fakeInfo);

        // Act
        DeviceInfoRequest request = new DeviceInfoRequest("device-full-001");
        IotDeviceInfo result = service.getDeviceInfo(request);

        // Assert
        assertEquals("device-full-001", result.getDeviceId());
        assertEquals("SmartSensor", result.getProductName());
        assertEquals("温湿度传感器 #1", result.getDeviceName());
        assertEquals(25.5, (Double) result.getDeviceData().get("temperature"));
        assertEquals("2.0.1", result.getServices().get("ota").get("version"));
    }

    @Test
    void testGetDeviceInfo_EmptyDeviceId() {
        // Act & Assert
        DeviceInfoRequest request = new DeviceInfoRequest("");
        assertThrows(IllegalArgumentException.class, () -> service.getDeviceInfo(request));
        verifyNoInteractions(httpClient);
    }

    @Test
    void testGetDeviceInfo_NullRequest() {
        // Act & Assert
        assertThrows(IllegalArgumentException.class, () -> service.getDeviceInfo(null));
        verifyNoInteractions(httpClient);
    }

    @Test
    void testGetDeviceInfo_ApiError() {
        // Arrange
        when(httpClient.post(eq("/iot/device/info"), any(DeviceInfoRequest.class), eq(IotDeviceInfo.class)))
                .thenThrow(new RuntimeException("device not found"));

        // Act & Assert
        DeviceInfoRequest request = new DeviceInfoRequest("nonexistent-device");
        assertThrows(RuntimeException.class, () -> service.getDeviceInfo(request));
    }
}