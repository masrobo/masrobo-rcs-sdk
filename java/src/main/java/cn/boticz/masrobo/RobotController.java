package cn.boticz.masrobo;

import cn.boticz.masrobo.service.IotDeviceService;
import cn.boticz.masrobo.client.Config;
import cn.boticz.masrobo.client.OpenHttpClient;


public class RobotController {
    private final IotDeviceService iotDevice;

    public RobotController(Config config) {
        OpenHttpClient httpClient = new OpenHttpClient(config);
        this.iotDevice = new IotDeviceService(httpClient);
    }

    public IotDeviceService getIotDevice() {
        return iotDevice;
    }
}

