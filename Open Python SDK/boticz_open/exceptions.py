class APIError(Exception):
    def __init__(self, status_code, code, message, raw_body=None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.raw_body = raw_body
        if code:
            text = f"open api error: status={status_code} code={code} message={message}"
        else:
            text = f"open api error: status={status_code} message={message}"
        super().__init__(text)

