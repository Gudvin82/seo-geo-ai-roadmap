from __future__ import annotations


def _create_workspace_and_project(
    client,
    auth_headers: dict[str, str],
) -> tuple[int, int]:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Operator", "slug": "operator"},
        headers=auth_headers,
    )
    workspace_id = workspace.json()["id"]
    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace_id,
            "name": "Operator Site",
            "website_url": "https://example.com",
            "market": "Global",
            "language": "en",
            "project_type": "saas",
            "audit_preset": "global_multilingual",
        },
        headers=auth_headers,
    )
    return workspace_id, project.json()["id"]


def test_readyz_does_not_expose_database_url(client) -> None:
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ok"}


def test_prompt_library_sov_notifications_and_export(
    client,
    auth_headers: dict[str, str],
) -> None:
    workspace_id, project_id = _create_workspace_and_project(client, auth_headers)

    prompt_set = client.post(
        "/api/v1/prompt-sets",
        json={
            "workspace_id": workspace_id,
            "name": "Audit handoff",
            "purpose": "audit reasoning",
            "output_format": "markdown plan",
            "model_recommendation": "gpt-4.1 / claude / ollama",
            "risk_notes": "Human review required.",
            "human_review_required": True,
            "prompt_items": ["Check facts", "Return action plan"],
        },
        headers=auth_headers,
    )
    assert prompt_set.status_code == 200

    prompt_sets = client.get(
        f"/api/v1/prompt-sets?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert prompt_sets.status_code == 200
    assert prompt_sets.json()[0]["purpose"] == "audit reasoning"

    notification = client.post(
        "/api/v1/notifications",
        json={
            "workspace_id": workspace_id,
            "channel_type": "webhook",
            "label": "Ops webhook",
            "target_url": "https://example.com/hook",
            "events": ["sov.completed"],
            "is_enabled": True,
        },
        headers=auth_headers,
    )
    assert notification.status_code == 200

    notifications = client.get(
        f"/api/v1/notifications?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert notifications.status_code == 200
    assert notifications.json()[0]["label"] == "Ops webhook"

    sov = client.post(
        "/api/v1/sov/check",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "brand": "Operator",
            "queries": ["seo ai visibility", "geo audit"],
            "providers": ["chatgpt", "perplexity"],
            "language": "en",
        },
        headers=auth_headers,
    )
    assert sov.status_code == 200
    sov_id = sov.json()["id"]

    history = client.get(
        f"/api/v1/sov/history?project_id={project_id}",
        headers=auth_headers,
    )
    assert history.status_code == 200
    assert history.json()[0]["brand"] == "Operator"

    sov_run = client.get(f"/api/v1/sov/{sov_id}", headers=auth_headers)
    assert sov_run.status_code == 200
    assert sov_run.json()["status"] == "completed"

    project_package = client.get(
        f"/api/v1/exports/project-package?project_id={project_id}",
        headers=auth_headers,
    )
    assert project_package.status_code == 200
    payload = project_package.json()
    assert payload["project"]["id"] == project_id
    assert "sov_runs" in payload
