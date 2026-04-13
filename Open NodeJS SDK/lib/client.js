const { createConfig } = require('./config');
const { decodeSuccessData, createAPIError } = require('./base');

class Client {
  constructor(config = {}) {
    const normalized = createConfig(config);
    this.baseURL = normalized.baseURL;
    this.token = normalized.token;
    this.httpClient = normalized.httpClient;
  }

  async request(method, path, { query, body } = {}) {
    const response = await this.httpClient.request({
      method,
      url: `${this.baseURL}/${String(path).replace(/^\/+/, '')}`,
      params: query,
      data: body,
      headers: {
        Accept: 'application/json',
        'X-Token': this.token,
        ...(body ? { 'Content-Type': 'application/json' } : {}),
      },
      validateStatus: () => true,
    });

    if (response.status >= 400 || (response.data || {}).code !== 200) {
      throw createAPIError(response.status, response.data, response.data);
    }

    return decodeSuccessData((response.data || {}).data);
  }
}

module.exports = { Client };
