import { APIError } from './error';

export const SUCCESS_CODE = 200;

export function decodeSuccessData(data: any): any {
  return data == null ? null : data;
}

export function createAPIError(statusCode: number, envelope: any, rawBody: any): APIError {
  const payload = envelope || {};
  return new APIError(
    statusCode,
    payload.code || 0,
    payload.msg || 'request failed',
    rawBody,
  );
}