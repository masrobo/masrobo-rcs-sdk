from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Config:
    base_url: str
    token: str
    session: Optional[requests.Session] = None

    def normalized_base_url(self) -> str:
        base_url = (self.base_url or "").strip().rstrip("/")
        if not base_url:
            raise ValueError("base_url is required")
        return base_url

    def normalized_token(self) -> str:
        token = (self.token or "").strip()
        if not token:
            raise ValueError("token is required")
        return token

    def normalized_session(self) -> requests.Session:
        return self.session or requests.Session()

