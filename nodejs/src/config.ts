import axios, { AxiosInstance, CreateAxiosDefaults } from 'axios';

export type ConfigOptions = {
  baseURL: string;
  token: string;
  axiosOptions?: CreateAxiosDefaults;
}

export interface Config {
  baseURL: string;
  token: string;
  axios: AxiosInstance;
}

export function createConfig(config: ConfigOptions): Config {
  const { baseURL, token, axiosOptions } = config;
  if (!baseURL || !String(baseURL).trim()) {
    throw new Error('baseURL is required');
  }
  if (!token || !String(token).trim()) {
    throw new Error('token is required');
  }

  return {
    baseURL: String(baseURL).trim().replace(/\/+$/, ''),
    token: String(token).trim(),
    axios: axios.create(axiosOptions ?? { timeout: 30000 }),
  };
}