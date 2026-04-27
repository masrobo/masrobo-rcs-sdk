import requests

from .base import SUCCESS_CODE, decode_success_data
from .config import Config
from .exceptions import APIError


class Client:
    def __init__(self, config: Config):
        self.base_url = config.normalized_base_url()
        self.token = config.generate_jwt_token()
        self.session = config.normalized_session()

    def request(self, method: str, path: str, params=None, data=None):
        print(f"request: {method} {self.base_url}/{path.lstrip('/')} {params} {data}")
        response = self.session.request(
            method=method,
            url=f"{self.base_url}/{path.lstrip('/')}",
            params=params,
            json=data,
            headers={
                "Accept": "application/json",
                "X-Token": self.token,
            },
            timeout=30,
        )

        raw = response.text
        try:
            envelope = response.json() if raw else {}
        except ValueError:
            envelope = {}

        if response.status_code >= 400 or envelope.get("code") != SUCCESS_CODE:
            raise APIError(response.status_code, envelope.get("code", 0), envelope.get("msg", "request failed"), raw)

        return decode_success_data(envelope.get("data"))
