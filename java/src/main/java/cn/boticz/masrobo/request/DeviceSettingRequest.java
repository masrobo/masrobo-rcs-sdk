package cn.boticz.masrobo.request;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;


@Data
public class DeviceSettingRequest {
    @JsonProperty("device_id")
    private String deviceId; // Device ID

    @JsonProperty("settings")
    private String settings; // JSON string of settings, e.g. {"temperature":{"max_value":30,"min_value":10,"calibration":0},"humidity":{"max_value":80,"min_value":20,"calibration":0},"data_recording_interval":5,"reporting_interval":10,"alert_interval":15,"alert_battery":10}
}