from __future__ import annotations


def _create_workspace_and_project(
    client, auth_headers: dict[str, str]
) -> tuple[int, int]:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Ops Workspace", "slug": "ops-workspace-v330"},
        headers=auth_headers,
    )
    workspace_id = workspace.json()["id"]
    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace_id,
            "name": "Ops Site",
            "website_url": "https://example.com",
            "market": "Global",
            "language": "en",
            "project_type": "saas",
            "audit_preset": "global_multilingual",
        },
        headers=auth_headers,
    )
    return workspace_id, project.json()["id"]


def test_fact_drift_api_detects_mismatch(client) -> None:
    response = client.post(
        "/api/v1/tools/fact-drift",
        json={
            "surfaces": [
                {
                    "name": "website",
                    "content": "Our office is in Moscow and support is available 24/7.",
                },
                {
                    "name": "schema",
                    "content": "The company is based in London and support works business hours only.",
                },
            ]
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["surface_count"] == 2
    assert payload["drift_items"]


def test_scheduled_checks_expose_execution_model(client, auth_headers) -> None:
    workspace_id, project_id = _create_workspace_and_project(client, auth_headers)
    created = client.post(
        "/api/v1/scheduled-checks",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "name": "Weekly llms review",
            "frequency": "weekly",
            "check_type": "llms",
            "is_enabled": True,
            "config": {
                "schedule_mode": "github_actions",
                "schedule_expression": "0 9 * * 1",
            },
        },
        headers=auth_headers,
    )
    assert created.status_code == 200
    payload = created.json()
    assert payload["schedule_mode"] == "github_actions"
    assert payload["execution_path"]
    assert payload["last_status"] == "queued"
    assert payload["limitations"]


def test_notification_endpoint_exposes_retry_policy(client, auth_headers) -> None:
    workspace_id, _ = _create_workspace_and_project(client, auth_headers)
    created = client.post(
        "/api/v1/notifications",
        json={
            "workspace_id": workspace_id,
            "channel_type": "webhook",
            "label": "Ops Hook",
            "target_url": "https://example.com/hook",
            "events": ["audit.completed"],
            "is_enabled": True,
        },
        headers=auth_headers,
    )
    assert created.status_code == 200
    assert created.json()["retry_policy"]["max_attempts"] == 3


def test_cms_writeback_attempt_respects_safe_mode(client, auth_headers) -> None:
    workspace_id, project_id = _create_workspace_and_project(client, auth_headers)
    audit = client.post(
        "/api/v1/audit-runs/run",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "domain_or_url": "https://example.com",
            "report_language": "en",
            "selected_checks": ["factual_consistency"],
            "selected_providers": [],
            "mode": "quick",
        },
        headers=auth_headers,
    )
    assert audit.status_code == 200
    connector = client.post(
        "/api/v1/cms",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "cms_type": "wordpress",
            "label": "Main WP",
            "base_url": "https://example.com",
            "writeback_mode": "human_approved_publish",
        },
        headers=auth_headers,
    )
    assert connector.status_code == 200
    payload = connector.json()
    assert payload["retry_policy"]["terminal_state"] == "dead"

    attempt = client.post(
        f"/api/v1/cms/{payload['id']}/writeback-attempt",
        headers=auth_headers,
    )
    assert attempt.status_code == 200
    attempt_payload = attempt.json()
    assert attempt_payload["status"] == "awaiting_human_approval"
    assert attempt_payload["attempts"] >= 1
