# Open Python SDK

`Open Python SDK` is a lightweight Python client for the Boticz Open API.

## Features

- `X-Token` authentication
- Unified HTTP client and error handling
- IoT device APIs
  - Get latest device data
  - Send device command
  - Bind device
  - Update device settings

# 如何使用

## 安装

```bash
pip3 install boticz_rcs_sdk
```

## Quick Start

```python
from boticz_rcs_sdk import RobotController, TopicDeviceData, GetLatestDeviceDataRequest

client = RobotController(
    base_url="https://api.boticz.cn/open",
    token="your-x-token",
)

resp = client.IotDevice.get_latest_device_data(
    GetLatestDeviceDataRequest(
        product_name="demo_product",
        device_id="device001",
        topic_name=TopicDeviceData,
    )
)

print(resp)
```

## Available APIs

### Get latest device data

```python
from boticz_open import TopicScreenshot, GetLatestDeviceDataRequest

client.IotDevice.get_latest_device_data(
    GetLatestDeviceDataRequest(
        product_name="demo_product",
        device_id="device001",
        topic_name=TopicScreenshot,
    )
)
```

### Send device command

```python
from boticz_open import TopicRemoteControl, SendDeviceCommandRequest

client.IotDevice.send_device_command(
    SendDeviceCommandRequest(
        command="reboot",
        parameter='{"delay":1}',
        device_id="device001",
        product_name="demo_product",
        topic_name=TopicRemoteControl,
    )
)
```

### Bind device

```python
from boticz_open import BindDeviceRequest

client.IotDevice.bind_device(BindDeviceRequest(device_id="device001"))
```

### Update device settings

```python
from boticz_open import DeviceSettingRequest, TemperatureSetting, HumiditySetting

client.IotDevice.setting(
    DeviceSettingRequest(
        device_id="device001",
        temperature=TemperatureSetting(max_value=30, min_value=10, calibration=0),
        humidity=HumiditySetting(max_value=80, min_value=20, calibration=0),
        data_recording_interval=5,
        reporting_interval=10,
        alert_interval=15,
        alert_battery=10,
    )
)
```

## Error Handling

```python
from boticz_open import APIError

try:
    client.IotDevice.get_latest_device_data(
        GetLatestDeviceDataRequest(
            product_name="demo_product",
            device_id="device001",
            topic_name=TopicDeviceData,
        )
    )
except APIError as err:
    print(err.status_code, err.code, err.message)
```
