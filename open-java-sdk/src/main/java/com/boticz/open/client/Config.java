package com.boticz.open.client;

import java.net.http.HttpClient;
import java.time.Duration;

public class Config {
    private static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(30);

    private final String baseUrl;
    private final String token;
    private final HttpClient httpClient;

    public Config(String baseUrl, String token) {
        this(baseUrl, token, null);
    }

    public Config(String baseUrl, String token, HttpClient httpClient) {
        this.baseUrl = require(baseUrl, "baseUrl");
        this.token = require(token, "token");
        this.httpClient = httpClient != null
                ? httpClient
                : HttpClient.newBuilder().connectTimeout(DEFAULT_TIMEOUT).build();
    }

    public String getBaseUrl() {
        return baseUrl.replaceAll("/+$", "");
    }

    public String getToken() {
        return token;
    }

    public HttpClient getHttpClient() {
        return httpClient;
    }

    private static String require(String value, String name) {
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException(name + " is required");
        }
        return value.trim();
    }
}

