package masrobo

import "time"

// LatestDeviceDataRecord is the latest data record returned by the Open API.
type LatestDeviceDataRecord struct {
	RawTopicName string    `json:"raw_topic_name"`
	Payload      any       `json:"payload,omitempty"`
	URL          string    `json:"url,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
}

// GetLatestDeviceDataResponse is the SDK response for the latest device data API.
type GetLatestDeviceDataResponse struct {
	ProductName string                  `json:"product_name"`
	DeviceID    string                  `json:"device_id"`
	TopicName   string                  `json:"topic_name"`
	Record      *LatestDeviceDataRecord `json:"record"`
}
