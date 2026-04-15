package boticzopen

const (
	TopicDeviceData    = "device_data"
	TopicScreenshot    = "screenshot"
	TopicRemoteControl = "remote_control"
)

// GetLatestDeviceDataRequest is the request for querying the latest device data.
type GetLatestDeviceDataRequest struct {
	ProductName string `url:"product_name" validate:"required"`
	DeviceID    string `url:"device_id" validate:"required"`
	TopicName   string `url:"topic_name" validate:"required,oneof=device_data screenshot"`
}

// SendDeviceCommandRequest is the request for sending a remote command to a device.
type SendDeviceCommandRequest struct {
	Command     string `json:"command" validate:"required"`
	Parameter   string `json:"parameter" validate:"required"`
	DeviceID    string `json:"device_id" validate:"required"`
	ProductName string `json:"product_name" validate:"required"`
	TopicName   string `json:"topic_name" validate:"required,oneof=remote_control"`
}

// BindDeviceRequest is the request for binding a device to a user account.
type BindDeviceRequest struct {
	DeviceID string `json:"device_id" validate:"required"`
}

// TemperatureSetting is the temperature configuration for device settings.
type TemperatureSetting struct {
	MaxValue    float32 `json:"max_value" validate:"required"`
	MinValue    float32 `json:"min_value" validate:"required"`
	Calibration float32 `json:"calibration" validate:"required"`
}

// HumiditySetting is the humidity configuration for device settings.
type HumiditySetting struct {
	MaxValue    float32 `json:"max_value" validate:"required"`
	MinValue    float32 `json:"min_value" validate:"required"`
	Calibration float32 `json:"calibration" validate:"required"`
}

// DeviceSettingRequest is the request for updating device settings.
type DeviceSettingRequest struct {
	DeviceID              string             `json:"device_id" validate:"required"`
	Temperature           TemperatureSetting `json:"temperature" validate:"required"`
	Humidity              HumiditySetting    `json:"humidity" validate:"required"`
	DataRecordingInterval int64              `json:"data_recording_interval" validate:"required"`
	ReportingInterval     int64              `json:"reporting_interval" validate:"required"`
	AlertInterval         int64              `json:"alert_interval" validate:"required"`
}
