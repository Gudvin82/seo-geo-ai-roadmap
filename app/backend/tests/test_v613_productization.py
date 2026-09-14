from __future__ import annotations

from fastapi.testclient import TestClient


def _project(client: TestClient, headers: dict[str, str]) -> tuple[int, int]:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Product", "slug": "product"},
        headers=headers,
    )
    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace.json()["id"],
            "name": "Product Site",
            "website_url": "https://example.com",
            "market": "Global",
            "language": "en",
            "project_type": "technical_product_site",
            "audit_preset": "technical_product_site",
        },
        headers=headers,
    )
    return workspace.json()["id"], project.json()["id"]


def test_unified_report_is_persisted_and_exposed(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    workspace_id, project_id = _project(client, auth_headers)
    audit = client.post(
        "/api/v1/audit-runs/run",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "domain_or_url": "https://example.com",
            "selected_checks": ["entity_hierarchy_review"],
            "selected_providers": [],
            "report_language": "en",
            "mode": "quick",
        },
        headers=auth_headers,
    )
    assert audit.status_code == 200
    report = client.get(
        f"/api/v1/geo-intelligence/audit-runs/{audit.json()['audit_job_id']}/unified-report",
        headers=auth_headers,
    )
    assert report.status_code == 200, report.text
    payload = report.json()
    assert payload["report_type"] == "geo_intelligence_unified"
    assert payload["tasks"]["tasks"]
    assert payload["graph"]["nodes"]
    artifacts = client.get(
        f"/api/v1/artifacts?project_id={project_id}", headers=auth_headers
    )
    assert any(
        item["artifact_type"] == "unified_geo_intelligence_report"
        for item in artifacts.json()
    )


def test_integration_lifecycle_is_explicit(client: TestClient) -> None:
    response = client.get("/api/v1/integrations/lifecycle")
    assert response.status_code == 200
    payload = response.json()
    assert "production_ready" in payload["levels"]
    assert (
        "refresh-token recovery where OAuth applies"
        in payload["production_ready_requires"]
    )
