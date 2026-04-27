package com.boticz.masrobo.base;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ApiEnvelope<T> {
    @JsonProperty("code")
    private int code;

    @JsonProperty("msg")
    private String msg;

    @JsonProperty("data")
    private T data;

    public int getCode() {
        return code;
    }

    public String getMsg() {
        return msg;
    }

    public T getData() {
        return data;
    }
}

