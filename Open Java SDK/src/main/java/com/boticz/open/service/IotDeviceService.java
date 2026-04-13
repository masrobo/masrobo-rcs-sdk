package com.boticz.open.service;

import com.boticz.open.client.OpenHttpClient;
import com.boticz.open.request.BindDeviceRequest;
import com.boticz.open.request.DeviceSettingRequest;
import com.boticz.open.request.GetLatestDeviceDataRequest;
import com.boticz.open.request.SendDeviceCommandRequest;
import com.boticz.open.response.GetLatestDeviceDataResponse;
import com.boticz.open.validator.RequestValidator;

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
        RequestValidator.require(request.getTemperature(), "temperature");
        RequestValidator.require(request.getHumidity(), "humidity");
        httpClient.post("/iot/device/setting", request);
    }
}

