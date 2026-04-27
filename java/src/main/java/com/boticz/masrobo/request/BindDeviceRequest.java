package com.boticz.masrobo.request;

import com.fasterxml.jackson.annotation.JsonProperty;

public class BindDeviceRequest {
    @JsonProperty("device_id")
    private String deviceId;

    public BindDeviceRequest(String deviceId) {
        this.deviceId = deviceId;
    }

    public String getDeviceId() {
        return deviceId;
    }
}

