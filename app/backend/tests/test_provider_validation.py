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

    expanded_provider = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "openrouter",
            "label": "OpenRouter routing",
            "model": "openai/gpt-4.1-mini",
            "api_key_env_var": "OPENROUTER_API_KEY",
        },
        headers=auth_headers,
    )
    assert expanded_provider.status_code == 200

    local_gateway = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "litellm",
            "label": "LiteLLM local gateway",
            "model": "gpt-4.1-mini",
            "base_url": "http://litellm:4000/v1/chat/completions",
        },
        headers=auth_headers,
    )
    assert local_gateway.status_code == 200

    additional_online = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "huggingface",
            "label": "HF Router",
            "model": "openai/gpt-oss-20b",
            "api_key_env_var": "HUGGINGFACE_API_KEY",
        },
        headers=auth_headers,
    )
    assert additional_online.status_code == 200
