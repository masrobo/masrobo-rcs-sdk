export const TopicDeviceData = 'device_data';
export const TopicScreenshot = 'screenshot';
export const TopicRemoteControl = 'remote_control';

export type AddDeviceRequest = {
  project_name: string;
  device_id: string;
};

export type DeviceSettingRequest = {
  device_id: string;
  settings: string;
};
