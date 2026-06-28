from __future__ import annotations

from app.deps import TOKENS
from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient) -> None:
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "Demo-password-123A"},
    )
    assert register.status_code == 200
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "Demo-password-123A"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert login.json()["expires_in_seconds"] > 0
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "user@example.com"


def test_logout_revokes_token(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "logout@example.com", "password": "Demo-password-123A"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "logout@example.com", "password": "Demo-password-123A"},
    )
    token = login.json()["access_token"]
    assert token in TOKENS
    logout = client.post(
        "/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert logout.status_code == 200
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 401
