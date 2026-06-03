package cn.boticz.masrobo.base;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class BaseResponse<T> {
    @JsonProperty("code")
    private int code;

    @JsonProperty("msg")
    private String msg;

    @JsonProperty("data")
    private T data;
}
