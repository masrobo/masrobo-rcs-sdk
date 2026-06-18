package cn.boticz.masrobo.request;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AddDeviceRequest {
    @JsonProperty("project_name")
    private String projectName;

    @JsonProperty("device_id")
    private String deviceId;

    public AddDeviceRequest(String projectName, String deviceId) {
        this.projectName = projectName;
        this.deviceId = deviceId;
    }

    public String getProjectName() {
        return projectName;
    }

    public String getDeviceId() {
        return deviceId;
    }
}
