# Open NodeJS SDK

`Open NodeJS SDK` is a lightweight Node.js client for the Boticz Open API.

## Features

- `X-Token` authentication
- Unified HTTP client and error handling
- IoT device APIs
  - Get latest device data
  - Send device command
  - Bind device
  - Update device settings

## Install

Run `npm install` in this SDK directory.

## Quick Start

```js
import {
  RobotController,
  TopicDeviceData,
} from 'boticz-rcs-sdk';

async function main() {
  const client = new RobotController({
    baseURL: 'https://api.boticz.cn/open',
    token: 'your-x-token',
  });

  const resp = await client.IotDevice.getLatestDeviceData({
    product_name: 'demo_product',
    device_id: 'device001',
    topic_name: TopicDeviceData,
  });

  console.log(resp);
}

main();
```

## Available APIs

### Get latest device data

```js
await client.IotDevice.getLatestDeviceData({
  product_name: 'demo_product',
  device_id: 'device001',
  topic_name: TopicScreenshot,
});
```

### Send device command

```js
await client.IotDevice.sendDeviceCommand({
  product_name: 'demo_product',
  device_id: 'device001',
  topic_name: TopicRemoteControl,
  command: 'reboot',
  parameter: '{"delay":1}',
});
```

### Bind device

```js
await client.IotDevice.bindDevice({
  device_id: 'device001',
});
```

### Update device settings

```js
await client.IotDevice.setting({
  device_id: 'device001',
  temperature: {
    max_value: 30,
    min_value: 10,
    calibration: 0,
  },
  humidity: {
    max_value: 80,
    min_value: 20,
    calibration: 0,
  },
  data_recording_interval: 5,
  reporting_interval: 10,
  alert_interval: 15,
  alert_battery: 10,
});
```

## Error Handling

```js
try {
  await client.IotDevice.getLatestDeviceData({
    product_name: 'demo_product',
    device_id: 'device001',
    topic_name: TopicDeviceData,
  });
} catch (err) {
  if (err instanceof APIError) {
    console.log(err.statusCode, err.code, err.message);
  }
}
```
