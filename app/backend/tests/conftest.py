from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    temp_dir = tempfile.TemporaryDirectory()
    data_dir = Path(temp_dir.name)
    settings = Settings(
        database_url=f"sqlite:///{data_dir / 'test.db'}",
        artifact_root=str(data_dir / "artifacts"),
        secret_key="test-secret",
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
    temp_dir.cleanup()


@pytest.fixture()
def auth_headers(client: TestClient) -> dict[str, str]:
    client.post("/api/v1/auth/register", json={"email": "owner@example.com", "password": "password123"})
    login = client.post("/api/v1/auth/login", json={"email": "owner@example.com", "password": "password123"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
