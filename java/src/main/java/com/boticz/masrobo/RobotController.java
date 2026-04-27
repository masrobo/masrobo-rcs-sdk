package com.boticz.masrobo;

import com.boticz.masrobo.service.IotDeviceService;
import com.boticz.masrobo.client.Config;
import com.boticz.masrobo.client.OpenHttpClient;


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

