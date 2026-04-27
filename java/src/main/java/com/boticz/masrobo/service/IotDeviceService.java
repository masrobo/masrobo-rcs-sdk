package com.boticz.masrobo.service;

import com.boticz.masrobo.client.OpenHttpClient;
import com.boticz.masrobo.request.BindDeviceRequest;
import com.boticz.masrobo.request.DeviceSettingRequest;
import com.boticz.masrobo.request.GetLatestDeviceDataRequest;
import com.boticz.masrobo.request.SendDeviceCommandRequest;
import com.boticz.masrobo.response.GetLatestDeviceDataResponse;
import com.boticz.masrobo.validator.RequestValidator;

import java.util.LinkedHashMap;
import java.util.Map;

public class IotDeviceService {
    private final OpenHttpClient httpClient;

    public IotDeviceService(OpenHttpClient httpClient) {
        this.httpClient = httpClient;
    }

    public GetLatestDeviceDataResponse getLatestDeviceData(GetLatestDeviceDataRequest request) {
        RequestValidator.require(request, "request");
        RequestValidator.require(request.getProductName(), "productName");
        RequestValidator.require(request.getDeviceId(), "deviceId");
        RequestValidator.require(request.getTopicName(), "topicName");

        Map<String, Object> query = new LinkedHashMap<>();
        query.put("product_name", request.getProductName());
        query.put("device_id", request.getDeviceId());
        query.put("topic_name", request.getTopicName());
        return httpClient.get("/iot/device/data", query, GetLatestDeviceDataResponse.class);
    }

    public void sendDeviceCommand(SendDeviceCommandRequest request) {
        RequestValidator.require(request, "request");
        RequestValidator.require(request.getCommand(), "command");
        RequestValidator.require(request.getParameter(), "parameter");
        RequestValidator.require(request.getDeviceId(), "deviceId");
        RequestValidator.require(request.getProductName(), "productName");
        RequestValidator.require(request.getTopicName(), "topicName");
        httpClient.post("/iot/device/command", request);
    }

    public void bindDevice(BindDeviceRequest request) {
        RequestValidator.require(request, "request");
        RequestValidator.require(request.getDeviceId(), "deviceId");
        httpClient.post("/iot/device/bind", request);
    }

    public void setting(DeviceSettingRequest request) {
        RequestValidator.require(request, "request");
        RequestValidator.require(request.getDeviceId(), "deviceId");
        RequestValidator.require(request.getSettings(), "settings");
        httpClient.post("/iot/device/setting", request);
    }
}