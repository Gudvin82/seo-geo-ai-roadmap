from __future__ import annotations

from fastapi.testclient import TestClient


def _project(client: TestClient, headers: dict[str, str]) -> tuple[int, int]:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "GEO", "slug": "geo-runtime"},
        headers=headers,
    )
    workspace_id = workspace.json()["id"]
    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace_id,
            "name": "Example",
            "website_url": "https://example.com",
            "market": "Global",
            "language": "en",
            "project_type": "technical_product_site",
            "audit_preset": "technical_product_site",
        },
        headers=headers,
    )
    return workspace_id, project.json()["id"]


def test_geo_runtime_and_visibility_history(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    workspace_id, project_id = _project(client, auth_headers)
    audit = client.post(
        "/api/v1/audit-runs/run",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "domain_or_url": "https://example.com",
            "selected_checks": ["entity_hierarchy_review", "llms_txt"],
            "selected_providers": [],
            "report_language": "en",
            "mode": "quick",
        },
        headers=auth_headers,
    )
    assert audit.status_code == 200
    runtime = client.post(
        "/api/v1/geo-intelligence/runs",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "audit_run_id": audit.json()["audit_job_id"],
        },
        headers=auth_headers,
    )
    assert runtime.status_code == 200, runtime.text
    assert runtime.json()["contract_version"] == "v1"
    assert runtime.json()["report_artifact_id"]
    snapshot = {
        "workspace_id": workspace_id,
        "project_id": project_id,
        "target_url": "https://example.com",
        "query": "example service",
        "query_set": "brand",
        "provider": "operator-capture",
        "model": "manual",
        "evidence_type": "manual-review",
        "confidence": 0.4,
        "evidence": {"mentioned": False},
        "snapshot": {"mentioned": False},
    }
    first = client.post(
        "/api/v1/geo-intelligence/visibility-snapshots",
        json=snapshot,
        headers=auth_headers,
    )
    assert first.status_code == 200
    snapshot["snapshot"] = {"mentioned": True}
    second = client.post(
        "/api/v1/geo-intelligence/visibility-snapshots",
        json=snapshot,
        headers=auth_headers,
    )
    assert second.status_code == 200
    history = client.get(
        f"/api/v1/geo-intelligence/visibility-snapshots?project_id={project_id}",
        headers=auth_headers,
    )
    assert history.status_code == 200
    assert history.json()[0]["changes"]["status"] == "compared"


def test_geo_runtime_requires_completed_audit(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    workspace_id, project_id = _project(client, auth_headers)
    response = client.post(
        "/api/v1/geo-intelligence/runs",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "audit_run_id": 99999,
        },
        headers=auth_headers,
    )
    assert response.status_code == 404
