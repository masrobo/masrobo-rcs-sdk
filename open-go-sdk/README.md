# Open Go SDK

`Open Go SDK` is a lightweight Go client for the Boticz Open API.

## Features

- `X-Token` authentication
- Unified HTTP client and error handling
- IoT device APIs
  - Get latest device data
  - Send device command
  - Bind device
  - Update device settings

## Install

```bash
go get github.com/boticz/open-go-sdk
```

## Quick Start

```go
package main

import (
	"context"
	"log"

	boticzopen "github.com/boticz/open-go-sdk"
)

func main() {
	client, err := boticzopen.NewClient(boticzopen.Config{
		BaseURL: "https://api.boticz.cn/open",
		Token:   "your-x-token",
	})
	if err != nil {
		log.Fatal(err)
	}

	resp, err := client.IotDevice.GetLatestDeviceData(context.Background(), boticzopen.GetLatestDeviceDataRequest{
		ProductName: "demo_product",
		DeviceID:    "device001",
		TopicName:   boticzopen.TopicDeviceData,
	})
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("latest data: %+v", resp)
}
```

## Available APIs

### Get latest device data

```go
resp, err := client.IotDevice.GetLatestDeviceData(ctx, boticzopen.GetLatestDeviceDataRequest{
	ProductName: "demo_product",
	DeviceID:    "device001",
	TopicName:   boticzopen.TopicScreenshot,
})
```

### Send device command

```go
err = client.IotDevice.SendDeviceCommand(ctx, boticzopen.SendDeviceCommandRequest{
	ProductName: "demo_product",
	DeviceID:    "device001",
	TopicName:   boticzopen.TopicRemoteControl,
	Command:     "reboot",
	Parameter:   "{\"delay\":1}",
})
```

### Bind device

```go
err = client.IotDevice.BindDevice(ctx, boticzopen.BindDeviceRequest{
	DeviceID: "device001",
})
```

### Update device settings

```go
err = client.IotDevice.Setting(ctx, boticzopen.DeviceSettingRequest{
	DeviceID: "device001",
	Temperature: boticzopen.TemperatureSetting{
		MaxValue:    30,
		MinValue:    10,
		Calibration: 0,
	},
	Humidity: boticzopen.HumiditySetting{
		MaxValue:    80,
		MinValue:    20,
		Calibration: 0,
	},
	DataRecordingInterval: 5,
	ReportingInterval:     10,
	AlertInterval:         15,
})
```

## Error Handling

```go
if err != nil {
	var apiErr *boticzopen.APIError
	if errors.As(err, &apiErr) {
		log.Printf("status=%d code=%d message=%s", apiErr.StatusCode, apiErr.Code, apiErr.Message)
	}
}
```
