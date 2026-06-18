export type DeviceQRCodeInfo = {
  qrcode_url: string;
};

export function toLatestDeviceDataResponse(data: any): any {
  return data == null ? null : data;
}