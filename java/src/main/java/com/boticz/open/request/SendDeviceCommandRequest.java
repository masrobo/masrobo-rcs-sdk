package com.boticz.open.request;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SendDeviceCommandRequest {
    @JsonProperty("command")
    private String command;

    @JsonProperty("parameter")
    private String parameter;

    @JsonProperty("device_id")
    private String deviceId;

    @JsonProperty("product_name")
    private String productName;

    @JsonProperty("topic_name")
    private String topicName;

    public SendDeviceCommandRequest(String command, String parameter, String deviceId, String productName, String topicName) {
        this.command = command;
        this.parameter = parameter;
        this.deviceId = deviceId;
        this.productName = productName;
        this.topicName = topicName;
    }

    public String getCommand() {
        return command;
    }

    public String getParameter() {
        return parameter;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public String getProductName() {
        return productName;
    }

    public String getTopicName() {
        return topicName;
    }
}

