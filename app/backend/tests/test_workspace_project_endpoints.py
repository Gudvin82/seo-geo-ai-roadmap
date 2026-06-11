from __future__ import annotations

from fastapi.testclient import TestClient


def test_workspace_update_and_project_listing(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    created = client.post(
        "/api/v1/workspaces",
        json={"name": "Studio", "slug": "studio"},
        headers=auth_headers,
    )
    workspace_id = created.json()["id"]

    updated = client.put(
        f"/api/v1/workspaces/{workspace_id}",
        json={"client_report_title": "Client-facing audit"},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["client_report_title"] == "Client-facing audit"

    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace_id,
            "name": "Site",
            "website_url": "https://example.com",
            "market": "RU",
            "language": "ru",
            "project_type": "expert_site",
            "audit_preset": "personal_expert_brand",
        },
        headers=auth_headers,
    )
    assert project.status_code == 200

    listed = client.get(
        f"/api/v1/projects?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    members = client.get(
        f"/api/v1/workspaces/{workspace_id}/members",
        headers=auth_headers,
    )
    assert members.status_code == 200
    assert members.json()[0]["role"] == "owner"
