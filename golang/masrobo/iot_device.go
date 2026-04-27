package masrobo

import (
	"context"
	"net/http"
)

// IotDeviceService wraps IoT device related Open API endpoints.
type IotDeviceService struct {
	client *Client
}

// GetLatestDeviceData queries the latest device data or screenshot record.
func (s *IotDeviceService) GetLatestDeviceData(ctx context.Context, req GetLatestDeviceDataRequest) (*GetLatestDeviceDataResponse, error) {
	if err := validateRequest(req); err != nil {
		return nil, err
	}

	resp := &GetLatestDeviceDataResponse{}
	if err := s.client.do(ctx, http.MethodGet, "/iot/device/data", req, nil, resp); err != nil {
		return nil, err
	}

	return resp, nil
}

// SendDeviceCommand sends a remote control command to a device.
func (s *IotDeviceService) SendDeviceCommand(ctx context.Context, req SendDeviceCommandRequest) error {
	if err := validateRequest(req); err != nil {
		return err
	}

	return s.client.do(ctx, http.MethodPost, "/iot/device/command", nil, req, nil)
}

// BindDevice binds a device to the current application user.
func (s *IotDeviceService) BindDevice(ctx context.Context, req BindDeviceRequest) error {
	if err := validateRequest(req); err != nil {
		return err
	}

	return s.client.do(ctx, http.MethodPost, "/iot/device/bind", nil, req, nil)
}

// Setting updates device settings.
func (s *IotDeviceService) Setting(ctx context.Context, req DeviceSettingRequest) error {
	if err := validateRequest(req); err != nil {
		return err
	}

	return s.client.do(ctx, http.MethodPost, "/iot/device/setting", nil, req, nil)
}
