package com.boticz.masrobo.client;

import com.boticz.masrobo.base.ApiConstants;
import com.boticz.masrobo.base.ApiEnvelope;
import com.boticz.masrobo.error.ApiException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public class OpenHttpClient {
    private final Config config;
    private final ObjectMapper objectMapper;

    public OpenHttpClient(Config config) {
        this.config = config;
        this.objectMapper = new ObjectMapper()
                .findAndRegisterModules()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    }

    public <T> T get(String path, Map<String, Object> query, Class<T> responseType) {
        return execute("GET", path, query, null, responseType);
    }

    public void post(String path, Object body) {
        execute("POST", path, null, body, Void.class);
    }

    private <T> T execute(String method, String path, Map<String, Object> query, Object body, Class<T> responseType) {
        try {
            String token = config.generateJwtToken();
            HttpRequest.Builder builder = HttpRequest.newBuilder()
                    .uri(URI.create(buildUrl(path, query)))
                    .header("Accept", "application/json")
                    .header("X-Token", token);

            if (body != null) {
                builder.header("Content-Type", "application/json");
                builder.method(method, HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(body)));
            } else {
                builder.method(method, HttpRequest.BodyPublishers.noBody());
            }

            HttpResponse<String> response = config.getHttpClient().send(builder.build(), HttpResponse.BodyHandlers.ofString());
            String rawBody = response.body() == null ? "" : response.body();

            if (rawBody.isBlank()) {
                if (response.statusCode() >= 400) {
                    throw new ApiException(response.statusCode(), 0, "request failed", rawBody);
                }
                return null;
            }

            ApiEnvelope<?> envelope = objectMapper.readValue(rawBody, envelopeType());
            if (response.statusCode() >= 400 || envelope.getCode() != ApiConstants.SUCCESS_CODE) {
                throw new ApiException(response.statusCode(), envelope.getCode(), envelope.getMsg(), rawBody);
            }

            if (responseType == Void.class || envelope.getData() == null) {
                return null;
            }
            return objectMapper.convertValue(envelope.getData(), responseType);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("decode response body: " + e.getMessage(), e);
        } catch (IOException e) {
            throw new RuntimeException("send request: " + e.getMessage(), e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("send request interrupted", e);
        }
    }

    private String buildUrl(String path, Map<String, Object> query) {
        StringBuilder builder = new StringBuilder(config.getBaseUrl())
                .append("/")
                .append(path.replaceFirst("^/+", ""));
        if (query == null || query.isEmpty()) {
            return builder.toString();
        }

        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, Object> entry : query.entrySet()) {
            if (entry.getValue() == null) {
                continue;
            }
            String value = Objects.toString(entry.getValue(), "").trim();
            if (value.isEmpty()) {
                continue;
            }
            parts.add(encode(entry.getKey()) + "=" + encode(value));
        }
        if (!parts.isEmpty()) {
            builder.append("?").append(String.join("&", parts));
        }
        return builder.toString();
    }

    private String encode(String value) {
        return URLEncoder.encode(value, StandardCharsets.UTF_8);
    }

    private TypeReference<ApiEnvelope<Object>> envelopeType() {
        return new TypeReference<ApiEnvelope<Object>>() {};
    }
}