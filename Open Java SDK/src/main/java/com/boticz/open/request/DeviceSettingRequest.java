package com.boticz.open.request;

import com.fasterxml.jackson.annotation.JsonProperty;

public class DeviceSettingRequest {
    @JsonProperty("device_id")
    private String deviceId;

    @JsonProperty("temperature")
    private TemperatureSetting temperature;

    @JsonProperty("humidity")
    private HumiditySetting humidity;

    @JsonProperty("data_recording_interval")
    private long dataRecordingInterval;

    @JsonProperty("reporting_interval")
    private long reportingInterval;

    public DeviceSettingRequest(String deviceId, TemperatureSetting temperature, HumiditySetting humidity,
                                long dataRecordingInterval, long reportingInterval) {
        this.deviceId = deviceId;
        this.temperature = temperature;
        this.humidity = humidity;
        this.dataRecordingInterval = dataRecordingInterval;
        this.reportingInterval = reportingInterval;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public TemperatureSetting getTemperature() {
        return temperature;
    }

    public HumiditySetting getHumidity() {
        return humidity;
    }

    public long getDataRecordingInterval() {
        return dataRecordingInterval;
    }

    public long getReportingInterval() {
        return reportingInterval;
    }
}

