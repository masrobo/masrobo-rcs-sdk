import axios, { AxiosInstance, CreateAxiosDefaults } from 'axios';
import jwt from 'jsonwebtoken';

export type ConfigOptions = {
  baseURL: string;
  appId: string;
  appKey: string;
  axiosOptions?: CreateAxiosDefaults;
}

export interface Config {
  baseURL: string;
  appId: string;
  appKey: string;
  axios: AxiosInstance;
  generateJwtToken: () => string;
}

export function createConfig(config: ConfigOptions): Config {
  const { baseURL, appId, appKey, axiosOptions } = config;
  if (!baseURL || !String(baseURL).trim()) {
    throw new Error('BaseURL is required');
  }
  if (!appId || !String(appId).trim()) {
    throw new Error('AppId is required');
  }
  if (!appKey || !String(appKey).trim()) {
    throw new Error('AppKey is required');
  }

  const normalizedAppId = String(appId).trim();
  const normalizedAppKey = String(appKey).trim();

  return {
    baseURL: String(baseURL).trim().replace(/\/+$/, ''),
    appId: normalizedAppId,
    appKey: normalizedAppKey,
    axios: axios.create(axiosOptions ?? { timeout: 30000 }),
    generateJwtToken: () => {
      const payload = {
        app_id: normalizedAppId,
        app_key: normalizedAppKey,
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + 3600, // 1 hour expiration
      };
      return jwt.sign(payload, normalizedAppKey, { algorithm: 'HS256' });
    },
  };
}