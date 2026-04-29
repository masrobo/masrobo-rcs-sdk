package cn.boticz.masrobo.error;

public class ApiException extends RuntimeException {
    private final int statusCode;
    private final int code;
    private final String rawBody;

    public ApiException(int statusCode, int code, String message, String rawBody) {
        super(code != 0
                ? String.format("open api error: status=%d code=%d message=%s", statusCode, code, message)
                : String.format("open api error: status=%d message=%s", statusCode, message));
        this.statusCode = statusCode;
        this.code = code;
        this.rawBody = rawBody;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public int getCode() {
        return code;
    }

    public String getRawBody() {
        return rawBody;
    }
}

