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

    command_contract = client.get("/api/v1/tools/command-contract")
    assert command_contract.status_code == 200
    assert command_contract.json()["canonical_prefix"] == "/geo"

    logs = client.get(
        f"/api/v1/audit-logs?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert logs.status_code == 200

    integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "gsc",
            "label": "Primary GSC",
            "property_identifier": "sc-domain:example.com",
            "credentials_env_var": "GSC_SERVICE_ACCOUNT_JSON",
            "config": {},
        },
        headers=auth_headers,
    )
    assert integration.status_code == 200
    integration_id = integration.json()["id"]

    integration_sync = client.post(
        f"/api/v1/integrations/{integration_id}/sync",
        headers=auth_headers,
    )
    assert integration_sync.status_code == 200
    assert integration_sync.json()["last_sync_status"] == "completed"
    assert integration_sync.json()["readiness_tier"] == "production_guided"

    integration_contracts = client.get(
        "/api/v1/integrations/contracts", headers=auth_headers
    )
    assert integration_contracts.status_code == 200
    assert integration_contracts.json()["contracts"]

    cms = client.post(
        "/api/v1/cms",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "cms_type": "webflow",
            "label": "Marketing Webflow",
            "base_url": "https://example.com",
            "writeback_mode": "draft",
        },
        headers=auth_headers,
    )
    assert cms.status_code == 200
    cms_id = cms.json()["id"]

    cms_inventory = client.post(
        f"/api/v1/cms/{cms_id}/inventory",
        headers=auth_headers,
    )
    assert cms_inventory.status_code == 200
    assert cms_inventory.json()["last_sync_status"] == "completed"
    assert cms_inventory.json()["execution_mode"]

    cms_contracts = client.get("/api/v1/cms/contracts", headers=auth_headers)
    assert cms_contracts.status_code == 200
    assert cms_contracts.json()["contracts"]

    patch_pack = client.post(
        "/api/v1/deliverables/patch-pack",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "report_language": "en",
            "mode": "draft",
            "audience": "agency",
        },
        headers=auth_headers,
    )
    assert patch_pack.status_code == 200
    assert "issue_backlog" in patch_pack.json()["outputs"]

    client_pack = client.post(
        "/api/v1/deliverables/client-pack",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "report_language": "en",
            "mode": "draft",
            "audience": "founder",
        },
        headers=auth_headers,
    )
    assert client_pack.status_code == 200
    assert "delivery_summary" in client_pack.json()["outputs"]

    project_package = client.get(
        f"/api/v1/exports/project-package?project_id={project_id}",
        headers=auth_headers,
    )
    assert project_package.status_code == 200

    executive_dashboard = client.get(
        f"/api/v1/settings/executive-dashboard?project_id={project_id}",
        headers=auth_headers,
    )
    assert executive_dashboard.status_code == 200
    assert executive_dashboard.json()["executive_score"] >= 0

    product_modes = client.get("/api/v1/settings/product-modes", headers=auth_headers)
    assert product_modes.status_code == 200
    assert len(product_modes.json()["modes"]) >= 3

    imported = client.post(
        "/api/v1/exports/project-package/import",
        json={
            "workspace_id": workspace_id,
            "payload": project_package.json(),
        },
        headers=auth_headers,
    )
    assert imported.status_code == 200
    assert imported.json()["project_id"] > 0
