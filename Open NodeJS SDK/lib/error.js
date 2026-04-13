class APIError extends Error {
  constructor(statusCode, code, message, rawBody) {
    super(code
      ? `open api error: status=${statusCode} code=${code} message=${message}`
      : `open api error: status=${statusCode} message=${message}`);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.code = code;
    this.rawBody = rawBody;
  }
}

module.exports = { APIError };

