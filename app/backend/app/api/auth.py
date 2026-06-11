from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..config import load_settings
from ..database import get_db
from ..deps import create_user_token, get_current_user, revoke_token
from ..metrics import AUTH_REQUESTS
from ..models import User
from ..schemas import LoginRequest, TokenResponse, UserCreate, UserRead
from ..security import (
    LOGIN_RATE_LIMITER,
    hash_password,
    login_limit_key,
    password_policy_summary,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    AUTH_REQUESTS.labels(endpoint="register", status="attempt").inc()
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        AUTH_REQUESTS.labels(endpoint="register", status="duplicate").inc()
        raise HTTPException(status_code=400, detail="Email already registered.")
    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    AUTH_REQUESTS.labels(endpoint="register", status="success").inc()
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    settings = getattr(request.app.state, "settings", load_settings())
    client_host = request.client.host if request.client else None
    limiter_key = login_limit_key(payload.email, client_host)
    AUTH_REQUESTS.labels(endpoint="login", status="attempt").inc()
    if LOGIN_RATE_LIMITER.is_limited(
        limiter_key,
        settings.login_attempt_limit,
        settings.login_attempt_window_seconds,
    ):
        AUTH_REQUESTS.labels(endpoint="login", status="limited").inc()
        raise HTTPException(
            status_code=429,
            detail=(
                "Too many login attempts. Please wait before trying again. "
                f"Password policy: {password_policy_summary()}"
            ),
        )
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        LOGIN_RATE_LIMITER.register_failure(
            limiter_key,
            settings.login_attempt_window_seconds,
        )
        AUTH_REQUESTS.labels(endpoint="login", status="failure").inc()
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    LOGIN_RATE_LIMITER.reset(limiter_key)
    token_session, token = create_user_token(user, settings)
    AUTH_REQUESTS.labels(endpoint="login", status="success").inc()
    return TokenResponse(
        access_token=token,
        expires_at=token_session.expires_at,
        expires_in_seconds=settings.token_ttl_minutes * 60,
    )


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("/logout")
def logout(request: Request) -> dict[str, str]:
    authorization = request.headers.get("Authorization", "")
    if authorization.lower().startswith("bearer "):
        revoke_token(authorization.split(" ", 1)[1].strip())
    AUTH_REQUESTS.labels(endpoint="logout", status="success").inc()
    return {"message": "Signed out."}
