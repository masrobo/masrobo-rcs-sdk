package com.boticz.open.client;

import com.boticz.open.service.IotDeviceService;

public class OpenClient {
    private final IotDeviceService iotDevice;

    public OpenClient(Config config) {
        OpenHttpClient httpClient = new OpenHttpClient(config);
        this.iotDevice = new IotDeviceService(httpClient);
    }

    public IotDeviceService getIotDevice() {
        return iotDevice;
    }
}

