package com.boticz.masrobo.response;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GetLatestDeviceDataResponse {
    @JsonProperty("product_name")
    private String productName;

    @JsonProperty("device_id")
    private String deviceId;

    @JsonProperty("topic_name")
    private String topicName;

    @JsonProperty("record")
    private LatestDeviceDataRecord record;

    public String getProductName() {
        return productName;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public String getTopicName() {
        return topicName;
    }

    public LatestDeviceDataRecord getRecord() {
        return record;
    }
}

