# Masrobo RCS SDK

`Masrobo RCS SDK` is a lightweight Go client for the Masrobo RCS API.

## Features

- `X-Token` authentication using JWT tokens generated from AppID and AppKey
- Unified HTTP client and error handling
- IoT device APIs
  - Get latest device data
  - Send device command
  - Bind device
  - Update device settings

## Install

```bash
go get github.com/boticz/masrobo-rcs-sdk/masrobo
```

## Quick Start

```go
package main

import (
	"context"
	"log"

	sdk "github.com/boticz/masrobo-rcs-sdk/masrobo"
)

func main() {
	```go
ctrl, err := sdk.NewRcsController(sdk.Config{
	BaseURL: "https://api.boticz.cn/open",
	AppID:   "your-app-id",
	AppKey:  "your-app-key",
})
	})
	if err != nil {
		log.Fatal(err)
	}

	resp, err := ctrl.IotDevice.GetLatestDeviceData(context.Background(), sdk.GetLatestDeviceDataRequest{
		ProductName: "demo_product",
		DeviceID:    "device001",
		TopicName:   sdk.TopicDeviceData,
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
resp, err := ctrl.IotDevice.GetLatestDeviceData(ctx, sdk.GetLatestDeviceDataRequest{
	ProductName: "demo_product",
	DeviceID:    "device001",
	TopicName:   sdk.TopicScreenshot,
})
```

### Send device command

```go
err = ctrl.IotDevice.SendDeviceCommand(ctx, sdk.SendDeviceCommandRequest{
	ProductName: "demo_product",
	DeviceID:    "device001",
	TopicName:   sdk.TopicRemoteControl,
	Command:     "reboot",
	Parameter:   "{\"delay\":1}",
})
```

### Bind device

```go
err = ctrl.IotDevice.BindDevice(ctx, sdk.BindDeviceRequest{
	DeviceID: "device001",
})
```

### Update device settings

```go
type TemperatureSetting struct {
	MaxValue    float64 `json:"max_value"`
	MinValue    float64 `json:"min_value"`
	Calibration float64 `json:"calibration"`
}

type HumiditySetting struct {
	MaxValue    float64 `json:"max_value"`
	MinValue    float64 `json:"min_value"`
	Calibration float64 `json:"calibration"`
}

type CustomDeviceSettings struct {
	Temperature TemperatureSetting `json:"temperature"`
	Humidity HumiditySetting `json:"humidity"`
	DataRecordingInterval int `json:"data_recording_interval"`
	ReportingInterval int `json:"reporting_interval"`
	AlertInterval int `json:"alert_interval"`
	AlertBattery int `json:"alert_battery"`
}

var settings []byte
settings, err = json.Marshal(CustomDeviceSettings{
		Temperature: TemperatureSetting{
			MaxValue:    30,
			MinValue:    10,
			Calibration: 0,
		},
		Humidity: HumiditySetting{
			MaxValue:    80,
			MinValue:    20,
			Calibration: 0,
		},
		DataRecordingInterval: 5,
		ReportingInterval:     10,
		AlertInterval:         15,
		AlertBattery:          10,
	})
if err != nil {
	log.Fatal(err)
}

err = ctrl.IotDevice.Setting(ctx, sdk.DeviceSettingRequest{
	DeviceID: "device001",
	Settings: settings,
})
```

## Error Handling

```go
if err != nil {
	var apiErr *sdk.APIError
	if errors.As(err, &apiErr) {
		log.Printf("status=%d code=%d message=%s", apiErr.StatusCode, apiErr.Code, apiErr.Message)
	}
}
```