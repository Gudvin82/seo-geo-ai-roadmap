from __future__ import annotations

import secrets
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

PASSWORD_HASHER = PasswordHasher()


@dataclass
class TokenSession:
    user_id: int
    expires_at: datetime


class LoginRateLimiter:
    def __init__(self) -> None:
        self._attempts: dict[str, deque[datetime]] = {}

    def _prune(self, key: str, window_seconds: int) -> deque[datetime]:
        bucket = self._attempts.setdefault(key, deque())
        cutoff = datetime.utcnow() - timedelta(seconds=window_seconds)
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        return bucket

    def is_limited(self, key: str, limit: int, window_seconds: int) -> bool:
        return len(self._prune(key, window_seconds)) >= limit

    def register_failure(self, key: str, window_seconds: int) -> int:
        bucket = self._prune(key, window_seconds)
        bucket.append(datetime.utcnow())
        return len(bucket)

    def reset(self, key: str) -> None:
        self._attempts.pop(key, None)


LOGIN_RATE_LIMITER = LoginRateLimiter()


def hash_password(password: str) -> str:
    return PASSWORD_HASHER.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return PASSWORD_HASHER.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def issue_token() -> str:
    return secrets.token_urlsafe(32)


def build_token_expiry(ttl_minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=ttl_minutes)


def password_policy_summary() -> str:
    return (
        "At least 12 characters with uppercase, lowercase, and numeric "
        "characters. Avoid reused or public passwords."
    )


def login_limit_key(email: str, client_host: Optional[str]) -> str:
    return f"{email.strip().lower()}::{client_host or 'unknown'}"
