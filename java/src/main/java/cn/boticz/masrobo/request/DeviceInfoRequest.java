package cn.boticz.masrobo.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class DeviceInfoRequest {
    @JsonProperty("device_id")
    private String deviceId;

    public DeviceInfoRequest(String deviceId) {
        this.deviceId = deviceId;
    }
}
