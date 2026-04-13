package com.boticz.open.response;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.OffsetDateTime;

public class LatestDeviceDataRecord {
    @JsonProperty("raw_topic_name")
    private String rawTopicName;

    @JsonProperty("payload")
    private Object payload;

    @JsonProperty("url")
    private String url;

    @JsonProperty("created_at")
    private OffsetDateTime createdAt;

    public String getRawTopicName() {
        return rawTopicName;
    }

    public Object getPayload() {
        return payload;
    }

    public String getUrl() {
        return url;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }
}

