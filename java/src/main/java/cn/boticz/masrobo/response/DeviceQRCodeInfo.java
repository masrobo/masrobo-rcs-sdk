package cn.boticz.masrobo.response;

import com.fasterxml.jackson.annotation.JsonProperty;

public class DeviceQRCodeInfo {
    @JsonProperty("qrcode_url")
    private String qrcodeUrl;

    public DeviceQRCodeInfo() {
    }

    public String getQrcodeUrl() {
        return qrcodeUrl;
    }

    public void setQrcodeUrl(String qrcodeUrl) {
        this.qrcodeUrl = qrcodeUrl;
    }

    @Override
    public String toString() {
        return "DeviceQRCodeInfo{" +
                "qrcodeUrl='" + qrcodeUrl + '\'' +
                '}';
    }
}
