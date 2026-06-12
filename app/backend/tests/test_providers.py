from __future__ import annotations

import pytest
from app.providers.base import ProviderError
from app.providers.registry import PROVIDERS, build_provider
from fastapi.testclient import TestClient


def test_provider_update_flow(client: TestClient, auth_headers: dict[str, str]) -> None:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Providers", "slug": "providers"},
        headers=auth_headers,
    )
    workspace_id = workspace.json()["id"]
    created = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "openai",
            "label": "OpenAI Primary",
            "model": "gpt-4.1-mini",
            "is_enabled": True,
        },
        headers=auth_headers,
    )
    assert created.status_code == 200
    provider_id = created.json()["id"]

    updated = client.put(
        f"/api/v1/providers/{provider_id}",
        json={"label": "OpenAI Secondary", "is_enabled": False},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["label"] == "OpenAI Secondary"
    assert updated.json()["is_enabled"] is False


def test_provider_registry_contains_required_providers() -> None:
    for name in ("openai", "anthropic", "gemini", "perplexity"):
        assert name in PROVIDERS


def test_missing_key_raises_provider_error() -> None:
    provider = build_provider("openai", api_key="", model="gpt-4o-mini")
    with pytest.raises(ProviderError):
        provider.generate_text("hello")
