# Open Java SDK

`Open Java SDK` is a lightweight Java client for the Boticz Open API.

## Features

- `X-Token` authentication using JWT tokens generated from appId and appKey
- Unified HTTP client and error handling
- IoT device APIs
  - Get latest device data
  - Send device command
  - Bind device
  - Update device settings

## Install

Add dependency in your Maven project after publishing, or copy this module into your workspace.

## Quick Start

```java
import com.boticz.masrobo.client.Config;
import com.boticz.masrobo.RobotController;
import com.boticz.masrobo.request.GetLatestDeviceDataRequest;
import com.boticz.masrobo.request.Topics;

public class Main {
    public static void main(String[] args) {
        RobotController client = new RobotController(new Config(
                "https://api.boticz.cn/open",
                "your-app-id",
                "your-app-key"
        ));

        var resp = client.getIotDevice().getLatestDeviceData(
                new GetLatestDeviceDataRequest("demo_product", "device001", Topics.DEVICE_DATA)
        );

        System.out.println(resp.getProductName());
    }
}
```

## Available APIs

### Get latest device data

```java
client.getIotDevice().getLatestDeviceData(
        new GetLatestDeviceDataRequest("demo_product", "device001", Topics.SCREENSHOT)
);
```

### Send device command

```java
client.getIotDevice().sendDeviceCommand(
        new SendDeviceCommandRequest("reboot", "{\"delay\":1}", "device001", "demo_product", Topics.REMOTE_CONTROL)
);
```

### Bind device

```java
client.getIotDevice().bindDevice(new BindDeviceRequest("device001"));
```

### Update device settings

```java
import lombok.Data;

@Data
public class TemperatureSetting {
    @JsonProperty("max_value")
    private float maxValue;

    @JsonProperty("min_value")
    private float minValue;

    @JsonProperty("calibration")
    private float calibration;

}



@Data
public class HumiditySetting {
    @JsonProperty("max_value")
    private float maxValue;

    @JsonProperty("min_value")
    private float minValue;

    @JsonProperty("calibration")
    private float calibration;
}


@Data
public class CustomDeviceSetting {
    private TemperatureSetting temperature;
    private HumiditySetting humidity;
    
    @JsonProperty("data_recording_interval")
    private Integer dataRecordingInterval;
    
    @JsonProperty("reporting_interval")
    private Integer reportingInterval;
    
    @JsonProperty("alert_interval")
    private Integer alertInterval;
    
    @JsonProperty("alert_battery")
    private Integer alertBattery;
}

@Data
public class CustomDeviceSettingRequest extends DeviceSettingRequest {

    private CustomDeviceSetting customDeviceSetting;

    @Override
    public String getSettings() {
        // Convert to JSON string
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            return objectMapper.writeValueAsString(customDeviceSetting);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return "";
        }
    }
}      

var settings = new CustomDeviceSetting();
settings.setTemperature(new TemperatureSetting(30, 10, 0));
settings.setHumidity(new HumiditySetting(80, 20, 0));
settings.setDataRecordingInterval(5);
settings.setReportingInterval(10);
settings.setAlertInterval(15);
settings.setAlertBattery(10);

settings.getHumidity().setMaxValue(80).setMinValue(20).setCalibration(0));
settings.setDataRecordingInterval(5);
settings.setReportingInterval(10);
settings.setAlertInterval(15);
settings.setAlertBattery(10);

client.getIotDevice().setting(
        new CustomDeviceSettingRequest()
                .setDeviceId("device001")
                .setCustomDeviceSetting(settings)
);
```

## Error Handling

```java
try {
    client.getIotDevice().getLatestDeviceData(
            new GetLatestDeviceDataRequest("demo_product", "device001", Topics.DEVICE_DATA)
    );
} catch (ApiException e) {
    System.out.println(e.getStatusCode());
    System.out.println(e.getCode());
    System.out.println(e.getMessage());
}
```