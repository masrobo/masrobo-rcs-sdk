import { APIError } from './error';

export declare const SUCCESS_CODE = 200;
export declare function decodeSuccessData(data: any): any;
export declare function createAPIError(statusCode: number, envelope: any, rawBody: any): APIError;
