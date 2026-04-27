import { ConfigOptions, createConfig } from './config';
import { decodeSuccessData, createAPIError } from './base';
import { AxiosInstance } from 'axios';

export class Client {
  private baseURL: string;
  private config: ReturnType<typeof createConfig>;
  private axios: AxiosInstance;

  constructor(config: ConfigOptions) {
    const normalized = createConfig(config);
    this.baseURL = normalized.baseURL;
    this.config = normalized;
    this.axios = normalized.axios;
  }

  async request(method: string, path: string, { query, body }: { query?: any; body?: any } = {}) {
    const token = this.config.generateJwtToken();
    const response = await this.axios.request({
      method,
      url: `${this.baseURL}/${String(path).replace(/^\/+/, '')}`,
      params: query,
      data: body,
      headers: {
        Accept: 'application/json',
        'X-Token': token,
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