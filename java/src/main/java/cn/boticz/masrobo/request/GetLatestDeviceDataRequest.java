package cn.boticz.masrobo.request;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GetLatestDeviceDataRequest {
    @JsonProperty("product_name")
    private String productName;

    @JsonProperty("device_id")
    private String deviceId;

    @JsonProperty("topic_name")
    private String topicName;

    public GetLatestDeviceDataRequest(String productName, String deviceId, String topicName) {
        this.productName = productName;
        this.deviceId = deviceId;
        this.topicName = topicName;
    }

    public String getProductName() {
        return productName;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public String getTopicName() {
        return topicName;
    }
}

