package com.boticz.open.request;

import com.fasterxml.jackson.annotation.JsonProperty;

public class HumiditySetting {
    @JsonProperty("max_value")
    private float maxValue;

    @JsonProperty("min_value")
    private float minValue;

    @JsonProperty("calibration")
    private float calibration;

    public HumiditySetting(float maxValue, float minValue, float calibration) {
        this.maxValue = maxValue;
        this.minValue = minValue;
        this.calibration = calibration;
    }

    public float getMaxValue() {
        return maxValue;
    }

    public float getMinValue() {
        return minValue;
    }

    public float getCalibration() {
        return calibration;
    }
}

