from __future__ import annotations

from fastapi.testclient import TestClient


def test_provider_config_validation(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Agency", "slug": "agency-providers"},
        headers=auth_headers,
    )
    workspace_id = workspace.json()["id"]

    invalid = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "unknown",
            "label": "Bad config",
            "model": "not-real",
        },
        headers=auth_headers,
    )
    assert invalid.status_code == 422

    valid = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "openai",
            "label": "Primary OpenAI",
            "model": "gpt-4.1-mini",
            "api_key_env_var": "OPENAI_API_KEY",
        },
        headers=auth_headers,
    )
    assert valid.status_code == 200

    local_provider = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "ollama",
            "label": "Local Ollama",
            "model": "llama3.1",
            "base_url": "http://ollama:11434/v1/chat/completions",
        },
        headers=auth_headers,
    )
    assert local_provider.status_code == 200
