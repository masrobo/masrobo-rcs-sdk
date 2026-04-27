from dataclasses import dataclass
from typing import Optional
import jwt
import time

import requests


@dataclass
class Config:
    base_url: str
    app_id: str
    app_key: str
    session: Optional[requests.Session] = None

    def normalized_base_url(self) -> str:
        base_url = (self.base_url or "").strip().rstrip("/")
        if not base_url:
            raise ValueError("base_url is required")
        return base_url

    def normalized_app_id(self) -> str:
        app_id = (self.app_id or "").strip()
        if not app_id:
            raise ValueError("app_id is required")
        return app_id

    def normalized_app_key(self) -> str:
        app_key = (self.app_key or "").strip()
        if not app_key:
            raise ValueError("app_key is required")
        return app_key

    def generate_jwt_token(self) -> str:
        payload = {
            "app_id": self.normalized_app_id(),
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600  # 1 hour expiration
        }
        return jwt.encode(payload, self.normalized_app_key(), algorithm="HS256")

    def normalized_session(self) -> requests.Session:
        return self.session or requests.Session()