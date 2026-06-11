from __future__ import annotations

from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient) -> None:
    register = client.post("/api/v1/auth/register", json={"email": "user@example.com", "password": "password123"})
    assert register.status_code == 200
    login = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "user@example.com"
