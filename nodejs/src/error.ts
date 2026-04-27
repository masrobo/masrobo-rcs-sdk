export class APIError extends Error {
  public statusCode: number;
  public code: number;
  public rawBody: any;

  constructor(statusCode: number, code: number, message: string, rawBody: any) {
    super(code
      ? `open api error: status=${statusCode} code=${code} message=${message}`
      : `open api error: status=${statusCode} message=${message}`);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.code = code;
    this.rawBody = rawBody;
  }
}