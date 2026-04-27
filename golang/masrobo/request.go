package masrobo

type DeviceDataTopicNameEnums string

const (
	TopicDeviceData DeviceDataTopicNameEnums = "device_data" // Device data topic
	TopicScreenshot DeviceDataTopicNameEnums = "screenshot"  // Screenshot topic
)

type DeviceCommandTopicNameEnums string

const (
	TopicRemoteControl DeviceCommandTopicNameEnums = "remote_control" // Remote control topic
)

// GetLatestDeviceDataRequest is the request for querying the latest device data.
type GetLatestDeviceDataRequest struct {
	ProductName string                   `url:"product_name" validate:"required"`
	DeviceID    string                   `url:"device_id" validate:"required"`
	TopicName   DeviceDataTopicNameEnums `url:"topic_name" validate:"required,oneof=device_data screenshot"`
}

// SendDeviceCommandRequest is the request for sending a remote command to a device.
type SendDeviceCommandRequest struct {
	Command     string                      `json:"command" validate:"required"`
	Parameter   string                      `json:"parameter" validate:"required"`
	DeviceID    string                      `json:"device_id" validate:"required"`
	ProductName string                      `json:"product_name" validate:"required"`
	TopicName   DeviceCommandTopicNameEnums `json:"topic_name" validate:"required,oneof=remote_control"`
}

// BindDeviceRequest is the request for binding a device to a user account.
type BindDeviceRequest struct {
	DeviceID string `json:"device_id" validate:"required"`
}

// DeviceSettingRequest is the request for updating device settings.
type DeviceSettingRequest struct {
	DeviceID string `json:"device_id" validate:"required"` // Device ID
	Settings string `json:"settings" validate:"required"`  // JSON string of settings, e.g. {"temperature":{"max_value":30,"min_value":10,"calibration":0},"humidity":{"max_value":80,"min_value":20,"calibration":0},"data_recording_interval":5,"reporting_interval":10,"alert_interval":15,"alert_battery":10}
}
