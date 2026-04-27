package com.boticz.masrobo.validator;

public final class RequestValidator {
    private RequestValidator() {}

    public static void require(Object value, String name) {
        if (value == null) {
            throw new IllegalArgumentException(name + " is required");
        }
        if (value instanceof String && ((String) value).trim().isEmpty()) {
            throw new IllegalArgumentException(name + " is required");
        }
    }
}

