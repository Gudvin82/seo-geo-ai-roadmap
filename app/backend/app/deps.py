from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .config import Settings
from .database import get_db
from .models import User
from .security import TokenSession, build_token_expiry, issue_token

TOKENS: dict[str, TokenSession] = {}


def get_current_user(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")
    token = authorization.split(" ", 1)[1].strip()
    token_session = TOKENS.get(token)
    if not token_session:
        raise HTTPException(status_code=401, detail="Invalid token.")
    if token_session.expires_at <= datetime.utcnow():
        TOKENS.pop(token, None)
        raise HTTPException(status_code=401, detail="Token expired.")
    user = db.get(User, token_session.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


def get_optional_current_user(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    token_session = TOKENS.get(token)
    if not token_session or token_session.expires_at <= datetime.utcnow():
        return None
    return db.get(User, token_session.user_id)


def create_user_token(user: User, settings: Settings) -> tuple[TokenSession, str]:
    token = issue_token()
    token_session = TokenSession(
        user_id=user.id,
        expires_at=build_token_expiry(settings.token_ttl_minutes),
    )
    TOKENS[token] = token_session
    return token_session, token


def revoke_token(token: str) -> None:
    TOKENS.pop(token, None)
