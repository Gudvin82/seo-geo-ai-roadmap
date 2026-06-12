from __future__ import annotations

from fastapi.testclient import TestClient


def test_workspace_project_and_audit_flow(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    workspace = client.post(
        "/api/v1/workspaces",
        json={"name": "Agency", "slug": "agency"},
        headers=auth_headers,
    )
    assert workspace.status_code == 200
    workspace_id = workspace.json()["id"]

    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace_id,
            "name": "Example Site",
            "website_url": "https://example.com",
            "market": "Global",
            "language": "en",
            "project_type": "technical_product_site",
            "audit_preset": "technical_product_site",
        },
        headers=auth_headers,
    )
    assert project.status_code == 200
    project_id = project.json()["id"]

    facts = client.post(
        "/api/v1/brand-facts",
        json={
            "project_id": project_id,
            "name": "Truth Center",
            "facts_markdown": "# Facts\nExample Site is a technical product.",
            "approved_claims": "- reliable\n- structured",
            "numeric_facts": ["3 markets"],
            "markets": ["Global"],
            "languages": ["en"],
        },
        headers=auth_headers,
    )
    assert facts.status_code == 200

    audit = client.post(
        "/api/v1/audit-runs/run",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "domain_or_url": "https://example.com",
            "report_language": "en",
            "selected_checks": ["factual_consistency", "entity_hierarchy_review"],
            "selected_providers": ["ollama"],
            "mode": "quick",
        },
        headers=auth_headers,
    )
    assert audit.status_code == 200
    assert audit.json()["initial_status"] in {"queued", "completed"}

    audit_status = client.get(
        f"/api/v1/audit-runs/{audit.json()['audit_job_id']}",
        headers=auth_headers,
    )
    assert audit_status.status_code == 200
    findings = audit_status.json()["finding_groups"]
    assert findings
    assert "priority_score" in findings[0]
    assert "benchmark_status" in findings[0]

    retried = client.post(
        f"/api/v1/audit-runs/{audit.json()['audit_job_id']}/retry",
        headers=auth_headers,
    )
    assert retried.status_code == 200

    reports = client.get(
        f"/api/v1/reports?project_id={project_id}", headers=auth_headers
    )
    assert reports.status_code == 200
    if reports.json():
        report_json = reports.json()[0]["summary_json"]
        assert "benchmark_summary" in report_json

    artifacts = client.get(
        f"/api/v1/artifacts?project_id={project_id}", headers=auth_headers
    )
    assert artifacts.status_code == 200

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "discoverability_report_generations_total" in metrics.text

    logs = client.get(
        f"/api/v1/audit-logs?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert logs.status_code == 200
