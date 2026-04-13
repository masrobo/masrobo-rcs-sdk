const { APIError } = require('./error');

const SUCCESS_CODE = 200;

function decodeSuccessData(data) {
  return data == null ? null : data;
}

function createAPIError(statusCode, envelope, rawBody) {
  const payload = envelope || {};
  return new APIError(
    statusCode,
    payload.code || 0,
    payload.msg || 'request failed',
    rawBody,
  );
}

module.exports = {
  SUCCESS_CODE,
  decodeSuccessData,
  createAPIError,
};

