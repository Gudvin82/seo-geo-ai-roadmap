from __future__ import annotations

from app.services import scan_jobs
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
        assistant = client.post(
            f"/api/v1/reports/{reports.json()[0]['id']}/assistant",
            json={"question": "What should we do next?", "language": "en"},
            headers=auth_headers,
        )
        assert assistant.status_code == 200
        assert assistant.json()["follow_up_actions"]

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
    assert "/geo agent" in command_contract.json()["canonical_sequence"]

    contracts_catalog = client.get("/api/v1/contracts/catalog")
    assert contracts_catalog.status_code == 200
    assert len(contracts_catalog.json()["contracts"]) >= 6

    audit_contract = client.get("/api/v1/contracts/audit_run")
    assert audit_contract.status_code == 200
    assert audit_contract.json()["title"] == "Audit Run Contract"

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
    assert integration_sync.json()["ci_gates"]
    assert integration_sync.json()["production_flow"]

    integration_contracts = client.get(
        "/api/v1/integrations/contracts", headers=auth_headers
    )
    assert integration_contracts.status_code == 200
    assert integration_contracts.json()["contracts"]
    assert any(
        item["source_type"] == "crux"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "yandex_direct"
        for item in integration_contracts.json()["contracts"]
    )
    integration_plan = client.get(
        f"/api/v1/integrations/{integration_id}/readiness-plan",
        headers=auth_headers,
    )
    assert integration_plan.status_code == 200
    assert integration_plan.json()["ci_first_class"] is True
    integration_matrix = client.get(
        f"/api/v1/integrations/verification-matrix?project_id={project_id}",
        headers=auth_headers,
    )
    assert integration_matrix.status_code == 200
    assert integration_matrix.json()["rows"]
    assert any(
        item["surface_type"] == "integration"
        for item in integration_matrix.json()["rows"]
    )

    direct_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "yandex_direct",
            "label": "Yandex Direct Paid Demand",
            "property_identifier": "direct-account-1",
            "credentials_env_var": "YANDEX_DIRECT_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert direct_integration.status_code == 200
    direct_sync = client.post(
        f"/api/v1/integrations/{direct_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert direct_sync.status_code == 200
    assert direct_sync.json()["last_sync_status"] == "completed"

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
    change_request = client.post(
        "/api/v1/cms/change-requests",
        json={"connector_id": cms_id, "audit_run_id": audit.json()["audit_job_id"]},
        headers=auth_headers,
    )
    assert change_request.status_code == 200
    change_request_id = change_request.json()["id"]
    assert change_request.json()["status"] == "preview_ready"

    approved = client.post(
        f"/api/v1/cms/change-requests/{change_request_id}/approve",
        headers=auth_headers,
    )
    assert approved.status_code == 200
    applied = client.post(
        f"/api/v1/cms/change-requests/{change_request_id}/apply",
        headers=auth_headers,
    )
    assert applied.status_code == 200
    verified = client.post(
        f"/api/v1/cms/change-requests/{change_request_id}/verify",
        headers=auth_headers,
    )
    assert verified.status_code == 200
    assert verified.json()["status"] == "verified"

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

    trusted_target = client.post(
        "/api/v1/trusted-delivery-targets",
        json={
            "workspace_id": workspace_id,
            "label": "Trusted marketing repo",
            "repository": "Gudvin82/example-site",
            "base_branch": "main",
            "allowed_domains": ["https://example.com"],
            "auto_merge_mode": "trusted_after_checks",
            "required_checks": ["python-tests", "markdown-lint", "link-check"],
            "is_enabled": True,
        },
        headers=auth_headers,
    )
    assert trusted_target.status_code == 200

    pr_proposal = client.post(
        "/api/v1/deliverables/pr-proposal",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "trusted_target_id": trusted_target.json()["id"],
            "report_language": "en",
            "audience": "developer",
            "review_mode": "draft",
        },
        headers=auth_headers,
    )
    assert pr_proposal.status_code == 200
    assert pr_proposal.json()["auto_merge_eligible"] is True
    assert pr_proposal.json()["required_checks"]

    audit_tasks = client.get(
        f"/api/v1/tasks/audit-run/{audit.json()['audit_job_id']}",
        headers=auth_headers,
    )
    assert audit_tasks.status_code == 200
    assert audit_tasks.json()["tasks"]

    graph_snapshot = client.get(
        f"/api/v1/graph-runtime/audit-run/{audit.json()['audit_job_id']}",
        headers=auth_headers,
    )
    assert graph_snapshot.status_code == 200
    assert graph_snapshot.json()["nodes"]

    agent_contract = client.get("/api/v1/agent-mode/contract", headers=auth_headers)
    assert agent_contract.status_code == 200
    assert "agent-plan" in agent_contract.json()["supported_modes"]

    agent_overview = client.get(
        f"/api/v1/agent-mode/overview?project_id={project_id}",
        headers=auth_headers,
    )
    assert agent_overview.status_code == 200
    assert "safe_action_boundary" in agent_overview.json()

    agent_run = client.post(
        "/api/v1/agent-mode/runs",
        json={
            "project_id": project_id,
            "mode": "agent-plan",
            "source_type": "audit_run",
            "source_id": audit.json()["audit_job_id"],
            "benchmark": "b2b_saas",
        },
        headers=auth_headers,
    )
    assert agent_run.status_code == 200
    assert agent_run.json()["follow_up_tasks"]

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

    managed_boundary = client.get(
        "/api/v1/settings/managed-api-boundary",
        headers=auth_headers,
    )
    assert managed_boundary.status_code == 200
    assert managed_boundary.json()["primary_resources"]

    product_modes = client.get("/api/v1/settings/product-modes", headers=auth_headers)
    assert product_modes.status_code == 200
    assert len(product_modes.json()["modes"]) >= 4

    service_foundation = client.get(
        "/api/v1/settings/service-foundation", headers=auth_headers
    )
    assert service_foundation.status_code == 200
    assert service_foundation.json()["sso_starter_modes"]
    assert service_foundation.json()["billing_starter_modes"]

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


def test_telegram_webhook_path(client: TestClient, settings, monkeypatch) -> None:
    settings.allow_public_intake = True
    settings.allow_anonymous_submission = True
    settings.scanner_telegram_webhook_secret = "telegram-secret"
    monkeypatch.setattr(
        scan_jobs,
        "_launch_scan_job",
        lambda local_settings, job_id: scan_jobs._run_scan_job(local_settings, job_id),
    )
    monkeypatch.setattr(
        scan_jobs, "_deliver_notifications", lambda local_settings, row, artifacts: []
    )

    response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "message": {
                "chat": {"id": 123456},
                "text": "/geo audit https://example.com",
            }
        },
        headers={"X-Telegram-Bot-Api-Secret-Token": "telegram-secret"},
    )
    assert response.status_code == 200
    assert response.json()["action"] == "audit"
    assert response.json()["scan_job_id"] > 0
