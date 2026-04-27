export declare class APIError extends Error {
    statusCode: number;
    code: number;
    rawBody: any;
    constructor(statusCode: number, code: number, message: string, rawBody: any);
}
