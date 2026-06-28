from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from app.config import Settings
from app.main import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_PASSWORD = "Demo-password-123A"


@pytest.fixture()
def settings() -> Settings:
    temp_dir = tempfile.TemporaryDirectory()
    data_dir = Path(temp_dir.name)
    settings_obj = Settings(
        database_url=f"sqlite:///{data_dir / 'test.db'}",
        artifact_root=str(data_dir / "artifacts"),
        secret_key="test-secret",
        token_ttl_minutes=60,
        login_attempt_limit=5,
        login_attempt_window_seconds=900,
        auto_create_schema=True,
    )
    settings_obj._temp_dir = temp_dir  # type: ignore[attr-defined]
    return settings_obj


@pytest.fixture()
def app(settings: Settings) -> FastAPI:
    app = create_app(settings)
    return app


@pytest.fixture()
def client(app: FastAPI, settings: Settings) -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
    settings._temp_dir.cleanup()  # type: ignore[attr-defined]


@pytest.fixture()
def auth_headers(client: TestClient) -> dict[str, str]:
    client.post(
        "/api/v1/auth/register",
        json={"email": "owner@example.com", "password": TEST_PASSWORD},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": TEST_PASSWORD},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
