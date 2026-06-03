package cn.boticz.masrobo.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.time.OffsetDateTime;
import java.util.Map;

@Data
public class IotDeviceInfo {
    @JsonProperty("id")
    private Long id;

    @JsonProperty("device_id")
    private String deviceId;

    @JsonProperty("iot_product_id")
    private Long iotProductId;

    @JsonProperty("product_name")
    private String productName;

    @JsonProperty("category_code")
    private String categoryCode;

    @JsonProperty("user_id")
    private Long userId;

    @JsonProperty("device_name")
    private String deviceName;

    @JsonProperty("active_type")
    private String[] activeType;

    @JsonProperty("status")
    private Integer status;

    @JsonProperty("active_time")
    private OffsetDateTime activeTime;

    @JsonProperty("deactive_time")
    private OffsetDateTime deactiveTime;

    @JsonProperty("application_id")
    private Long applicationId;

    @JsonProperty("developer_id")
    private Long developerId;

    @JsonProperty("app_id")
    private String appId;

    @JsonProperty("application_name")
    private String applicationName;

    @JsonProperty("developer_name")
    private String developerName;

    @JsonProperty("product_title")
    private String productTitle;

    @JsonProperty("device_data")
    private Map<String, Object> deviceData;

    @JsonProperty("device_data_time")
    private OffsetDateTime deviceDataTime;

    @JsonProperty("screenshot")
    private String screenshot;

    @JsonProperty("screenshot_time")
    private OffsetDateTime screenshotTime;

    @JsonProperty("services")
    private Map<String, Map<String, Object>> services;

    @JsonProperty("rel_role")
    private Integer relRole;

    @JsonProperty("rel_source")
    private String relSource;
}
