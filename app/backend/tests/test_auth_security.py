from __future__ import annotations

import tempfile
from pathlib import Path

from app.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient


def test_password_policy_is_enforced(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "weak@example.com", "password": "weakpass123"},
    )
    assert response.status_code == 422


def test_login_rate_limiting() -> None:
    temp_dir = tempfile.TemporaryDirectory()
    data_dir = Path(temp_dir.name)
    settings = Settings(
        database_url=f"sqlite:///{data_dir / 'rate-limit.db'}",
        artifact_root=str(data_dir / "artifacts"),
        secret_key="test-secret",
        token_ttl_minutes=60,
        login_attempt_limit=2,
        login_attempt_window_seconds=3600,
        auto_create_schema=True,
    )
    app = create_app(settings)
    with TestClient(app) as client:
        client.post(
            "/api/v1/auth/register",
            json={"email": "rate@example.com", "password": "Demo-password-123A"},
        )
        bad_login = {"email": "rate@example.com", "password": "WrongPass123"}
        assert client.post("/api/v1/auth/login", json=bad_login).status_code == 401
        assert client.post("/api/v1/auth/login", json=bad_login).status_code == 401
        limited = client.post("/api/v1/auth/login", json=bad_login)
        assert limited.status_code == 429
    temp_dir.cleanup()
