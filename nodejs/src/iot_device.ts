import { Client } from './client';
import { requireValue } from './validator';
import { toLatestDeviceDataResponse } from './response';

export class IotDeviceService {
  constructor(private client: Client) {}

  async getLatestDeviceData(request: any = {}) {
    requireValue(request.product_name, 'product_name');
    requireValue(request.device_id, 'device_id');
    requireValue(request.topic_name, 'topic_name');
    const data = await this.client.request('GET', '/iot/device/data', { query: request });
    return toLatestDeviceDataResponse(data);
  }

  async sendDeviceCommand(request: any = {}) {
    requireValue(request.command, 'command');
    requireValue(request.parameter, 'parameter');
    requireValue(request.device_id, 'device_id');
    requireValue(request.product_name, 'product_name');
    requireValue(request.topic_name, 'topic_name');
    await this.client.request('POST', '/iot/device/command', { body: request });
  }

  async bindDevice(request: any = {}) {
    requireValue(request.device_id, 'device_id');
    await this.client.request('POST', '/iot/device/bind', { body: request });
  }

  async setting(request: any = {}) {
    requireValue(request.device_id, 'device_id');
    requireValue(request.settings, 'settings');
    await this.client.request('POST', '/iot/device/setting', { body: request });
  }
}
