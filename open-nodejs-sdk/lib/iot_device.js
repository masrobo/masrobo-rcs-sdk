const { Client } = require('./client');
const { requireValue } = require('./validator');
const { toLatestDeviceDataResponse } = require('./response');

class IotDeviceService {
  constructor(client) {
    this.client = client;
  }

  async getLatestDeviceData(request = {}) {
    requireValue(request.product_name, 'product_name');
    requireValue(request.device_id, 'device_id');
    requireValue(request.topic_name, 'topic_name');
    const data = await this.client.request('GET', '/iot/device/data', { query: request });
    return toLatestDeviceDataResponse(data);
  }

  async sendDeviceCommand(request = {}) {
    requireValue(request.command, 'command');
    requireValue(request.parameter, 'parameter');
    requireValue(request.device_id, 'device_id');
    requireValue(request.product_name, 'product_name');
    requireValue(request.topic_name, 'topic_name');
    await this.client.request('POST', '/iot/device/command', { body: request });
  }

  async bindDevice(request = {}) {
    requireValue(request.device_id, 'device_id');
    await this.client.request('POST', '/iot/device/bind', { body: request });
  }

  async setting(request = {}) {
    requireValue(request.device_id, 'device_id');
    requireValue(request.temperature, 'temperature');
    requireValue(request.humidity, 'humidity');
    await this.client.request('POST', '/iot/device/setting', { body: request });
  }
}

class OpenClient extends Client {
  constructor(config) {
    super(config);
    this.IotDevice = new IotDeviceService(this);
  }
}

module.exports = {
  OpenClient,
  IotDeviceService,
};

