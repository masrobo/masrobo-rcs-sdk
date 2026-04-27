package com.boticz.masrobo.client;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

import java.net.http.HttpClient;
import java.time.Duration;
import java.util.Date;

public class Config {
    private static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(30);

    private final String baseUrl;
    private final String appId;
    private final String appKey;
    private final HttpClient httpClient;

    public Config(String baseUrl, String appId, String appKey) {
        this(baseUrl, appId, appKey, null);
    }

    public Config(String baseUrl, String appId, String appKey, HttpClient httpClient) {
        this.baseUrl = require(baseUrl, "baseUrl");
        this.appId = require(appId, "appId");
        this.appKey = require(appKey, "appKey");
        this.httpClient = httpClient != null
                ? httpClient
                : HttpClient.newBuilder().connectTimeout(DEFAULT_TIMEOUT).build();
    }

    public String getBaseUrl() {
        return baseUrl.replaceAll("/+$", "");
    }

    public String getAppId() {
        return appId;
    }

    public String getAppKey() {
        return appKey;
    }

    public HttpClient getHttpClient() {
        return httpClient;
    }

    public String generateJwtToken() {
        long now = System.currentTimeMillis();
        Date issuedAt = new Date(now);
        Date expiration = new Date(now + 3600000); // 1 hour expiration

        return Jwts.builder()
                .setSubject(appId)
                .claim("app_id", appId)
                .setIssuedAt(issuedAt)
                .setExpiration(expiration)
                .signWith(SignatureAlgorithm.HS256, appKey.getBytes())
                .compact();
    }

    private static String require(String value, String name) {
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException(name + " is required");
        }
        return value.trim();
    }
}