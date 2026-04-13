const axios = require('axios');

function createConfig({ baseURL, token, httpClient } = {}) {
  if (!baseURL || !String(baseURL).trim()) {
    throw new Error('baseURL is required');
  }
  if (!token || !String(token).trim()) {
    throw new Error('token is required');
  }

  return {
    baseURL: String(baseURL).trim().replace(/\/+$/, ''),
    token: String(token).trim(),
    httpClient: httpClient || axios.create({ timeout: 30000 }),
  };
}

module.exports = { createConfig };

