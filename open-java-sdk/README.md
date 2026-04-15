# Open Java SDK

`Open Java SDK` is a lightweight Java client for the Boticz Open API.

## Features

- `X-Token` authentication
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
import com.boticz.open.client.Config;
import com.boticz.open.client.OpenClient;
import com.boticz.open.request.GetLatestDeviceDataRequest;
import com.boticz.open.request.Topics;

public class Main {
    public static void main(String[] args) {
        OpenClient client = new OpenClient(new Config(
                "https://api.boticz.cn/open",
                "your-x-token"
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
client.getIotDevice().setting(
        new DeviceSettingRequest(
                "device001",
                new TemperatureSetting(30, 10, 0),
                new HumiditySetting(80, 20, 0),
                5,
                10
        )
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
