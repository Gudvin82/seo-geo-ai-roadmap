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
    assert integration_sync.json()["readiness_tier"] == "managed_runtime_ready"
    assert integration_sync.json()["ci_gates"]
    assert integration_sync.json()["production_flow"]
    assert integration_sync.json()["runtime_profile"]["runtime_level"]

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
    assert any(
        item["source_type"] == "google_ads"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "google_business_profile"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "keyword_research"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "competitor_intelligence"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "backlink_intelligence"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "rank_tracking"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "meta_ads"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "x_ads"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "x_organic"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "threads"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "reddit_mentions"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "tiktok_organic"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "vk_organic"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "telegram_channels"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "yandex_neuro"
        for item in integration_contracts.json()["contracts"]
    )
    assert any(
        item["source_type"] == "alice_ai_visibility"
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

    google_ads_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "google_ads",
            "label": "Google Ads Demand Layer",
            "property_identifier": "ads-account-1",
            "credentials_env_var": "GOOGLE_ADS_DEVELOPER_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert google_ads_integration.status_code == 200
    google_ads_sync = client.post(
        f"/api/v1/integrations/{google_ads_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert google_ads_sync.status_code == 200
    assert google_ads_sync.json()["last_sync_status"] == "completed"

    local_business_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "google_business_profile",
            "label": "Google Business Profile",
            "property_identifier": "location-1",
            "credentials_env_var": "GBP_SERVICE_ACCOUNT_JSON",
            "config": {},
        },
        headers=auth_headers,
    )
    assert local_business_integration.status_code == 200
    local_business_sync = client.post(
        f"/api/v1/integrations/{local_business_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert local_business_sync.status_code == 200

    keyword_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "keyword_research",
            "label": "Keyword Intelligence",
            "property_identifier": "keyword-set-1",
            "credentials_env_var": "KEYWORD_RESEARCH_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert keyword_integration.status_code == 200
    assert (
        client.post(
            f"/api/v1/integrations/{keyword_integration.json()['id']}/sync",
            headers=auth_headers,
        ).status_code
        == 200
    )

    competitor_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "competitor_intelligence",
            "label": "Competitor Intelligence",
            "property_identifier": "competitor-set-1",
            "credentials_env_var": "COMPETITOR_INTELLIGENCE_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert competitor_integration.status_code == 200
    assert (
        client.post(
            f"/api/v1/integrations/{competitor_integration.json()['id']}/sync",
            headers=auth_headers,
        ).status_code
        == 200
    )

    backlink_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "backlink_intelligence",
            "label": "Backlink Intelligence",
            "property_identifier": "authority-set-1",
            "credentials_env_var": "BACKLINK_INTELLIGENCE_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert backlink_integration.status_code == 200
    assert (
        client.post(
            f"/api/v1/integrations/{backlink_integration.json()['id']}/sync",
            headers=auth_headers,
        ).status_code
        == 200
    )

    rank_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "rank_tracking",
            "label": "Rank Tracking",
            "property_identifier": "rank-set-1",
            "credentials_env_var": "RANK_TRACKING_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert rank_integration.status_code == 200
    assert (
        client.post(
            f"/api/v1/integrations/{rank_integration.json()['id']}/sync",
            headers=auth_headers,
        ).status_code
        == 200
    )

    social_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "meta_ads",
            "label": "Meta Ads Amplification",
            "property_identifier": "meta-account-1",
            "credentials_env_var": "META_ADS_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert social_integration.status_code == 200
    social_sync = client.post(
        f"/api/v1/integrations/{social_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert social_sync.status_code == 200

    x_ads_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "x_ads",
            "label": "X Thought Leadership Ads",
            "property_identifier": "x-ads-account-1",
            "credentials_env_var": "X_ADS_TOKEN",
            "config": {},
        },
        headers=auth_headers,
    )
    assert x_ads_integration.status_code == 200
    x_ads_sync = client.post(
        f"/api/v1/integrations/{x_ads_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert x_ads_sync.status_code == 200

    vk_organic_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "vk_organic",
            "label": "VK Community Signals",
            "property_identifier": "vk-community-1",
            "credentials_env_var": "VK_ORGANIC_TOKEN",
            "config": {"refresh_minutes": 720, "managed_runtime_enabled": True},
        },
        headers=auth_headers,
    )
    assert vk_organic_integration.status_code == 200
    vk_organic_sync = client.post(
        f"/api/v1/integrations/{vk_organic_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert vk_organic_sync.status_code == 200

    telegram_channel_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "telegram_channels",
            "label": "Telegram Channel Demand",
            "property_identifier": "telegram-channel-1",
            "credentials_env_var": "TELEGRAM_CHANNEL_TOKEN",
            "config": {"refresh_minutes": 360, "managed_runtime_enabled": True},
        },
        headers=auth_headers,
    )
    assert telegram_channel_integration.status_code == 200
    telegram_channel_sync = client.post(
        f"/api/v1/integrations/{telegram_channel_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert telegram_channel_sync.status_code == 200

    yandex_neuro_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "yandex_neuro",
            "label": "Yandex Neuro Readiness",
            "property_identifier": "neuro-surface-1",
            "credentials_env_var": "YANDEX_NEURO_TOKEN",
            "config": {"refresh_minutes": 1440},
        },
        headers=auth_headers,
    )
    assert yandex_neuro_integration.status_code == 200
    yandex_neuro_sync = client.post(
        f"/api/v1/integrations/{yandex_neuro_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert yandex_neuro_sync.status_code == 200

    alice_visibility_integration = client.post(
        "/api/v1/integrations",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "alice_ai_visibility",
            "label": "Alice AI Visibility",
            "property_identifier": "alice-visibility-export-1",
            "credentials_env_var": "ALICE_AI_VISIBILITY_TOKEN",
            "config": {"refresh_minutes": 10080},
        },
        headers=auth_headers,
    )
    assert alice_visibility_integration.status_code == 200
    alice_visibility_sync = client.post(
        f"/api/v1/integrations/{alice_visibility_integration.json()['id']}/sync",
        headers=auth_headers,
    )
    assert alice_visibility_sync.status_code == 200
    assert (
        "share_of_voice" in alice_visibility_sync.json()["latest_snapshot"]["metrics"]
    )

    provider_config = client.post(
        "/api/v1/providers",
        json={
            "workspace_id": workspace_id,
            "provider_name": "openai",
            "label": "Primary OpenAI",
            "model": "gpt-4.1-mini",
            "api_key_env_var": "OPENAI_API_KEY",
            "base_url": None,
            "is_enabled": True,
        },
        headers=auth_headers,
    )
    assert provider_config.status_code == 200

    provider_catalog = client.get("/api/v1/providers/catalog", headers=auth_headers)
    assert provider_catalog.status_code == 200
    assert provider_catalog.json()["summary"]["total_supported"] >= 20

    provider_model_registry = client.get(
        "/api/v1/providers/model-registry",
        headers=auth_headers,
    )
    assert provider_model_registry.status_code == 200
    assert provider_model_registry.json()["registry_profiles"]["profiles"]

    provider_health = client.get(
        f"/api/v1/providers/health?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert provider_health.status_code == 200
    assert provider_health.json()["summary"]["configured"] >= 1

    provider_operating_center = client.get(
        f"/api/v1/providers/operating-center?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert provider_operating_center.status_code == 200
    assert provider_operating_center.json()["routing_policies"]

    integration_runtime_center = client.get(
        f"/api/v1/integrations/runtime-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert integration_runtime_center.status_code == 200
    assert integration_runtime_center.json()["summary"]["ru_market_surfaces"] >= 4

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
    assert executive_dashboard.json()["executive_layers"]["google_executive_layer"]
    assert executive_dashboard.json()["executive_layers"]["seo_intelligence_layer"][
        "connected"
    ]
    assert executive_dashboard.json()["executive_layers"]["ru_executive_layer"]
    assert executive_dashboard.json()["executive_layers"]["ru_geo_ai_layer"][
        "connected"
    ]
    assert executive_dashboard.json()["comparison_metrics"]["organic_demand"]
    assert executive_dashboard.json()["comparison_metrics"]["paid_demand"]
    assert (
        executive_dashboard.json()["comparison_metrics"]["ai_visibility"][
            "alice_ai_share_of_voice"
        ]
        >= 0
    )
    assert executive_dashboard.json()["weekly_narrative"]
    assert executive_dashboard.json()["benchmark_overlays"]
    assert executive_dashboard.json()["metrics"]["ru_geo_score"] >= 0
    assert executive_dashboard.json()["metrics"]["tracked_keywords"] > 0
    assert (
        executive_dashboard.json()["comparison_metrics"]["seo_intelligence"][
            "tracked_competitors"
        ]
        > 0
    )

    integration_detail = client.get(
        f"/api/v1/integrations/{google_ads_integration.json()['id']}/detail",
        headers=auth_headers,
    )
    assert integration_detail.status_code == 200
    assert integration_detail.json()["sync_logs"]
    assert integration_detail.json()["runtime_level"]

    organization = client.post(
        "/api/v1/saas/organizations",
        json={"name": "Demo Org", "slug": "demo-org"},
        headers=auth_headers,
    )
    assert organization.status_code == 200

    organization_switcher = client.get(
        "/api/v1/saas/organization-switcher",
        headers=auth_headers,
    )
    assert organization_switcher.status_code == 200
    assert organization_switcher.json()["workspaces"]

    tenant_profile = client.post(
        "/api/v1/saas/tenant-profiles",
        json={
            "workspace_id": workspace_id,
            "organization_id": organization.json()["id"],
            "tenant_name": "Demo Tenant",
            "plan_code": "growth",
            "plan_status": "active",
            "quota": {"monthly_syncs": 200},
            "usage": {"monthly_syncs_used": 12},
            "onboarding_state": {"auth": "done", "integrations": "partial"},
            "tenant_settings": {"managed_mode": False},
        },
        headers=auth_headers,
    )
    assert tenant_profile.status_code == 200

    tenant_overview = client.get(
        f"/api/v1/saas/tenant-overview?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert tenant_overview.status_code == 200
    assert tenant_overview.json()["roles_supported"]
    assert "usage_health" in tenant_overview.json()
    assert "quota_alerts" in tenant_overview.json()

    tenant_profile_updated = client.patch(
        f"/api/v1/saas/tenant-profiles/{tenant_profile.json()['id']}",
        json={
            "usage": {"monthly_syncs_used": 160},
            "tenant_settings": {"managed_mode": True, "executive_rollups": True},
        },
        headers=auth_headers,
    )
    assert tenant_profile_updated.status_code == 200
    assert tenant_profile_updated.json()["usage"]["monthly_syncs_used"] == 160

    workspace_catalog = client.get(
        "/api/v1/saas/workspace-catalog",
        headers=auth_headers,
    )
    assert workspace_catalog.status_code == 200
    assert workspace_catalog.json()["items"]

    api_key = client.post(
        "/api/v1/saas/api-keys",
        json={
            "workspace_id": workspace_id,
            "label": "Automation key",
            "scopes": ["scanner:read", "reports:read"],
        },
        headers=auth_headers,
    )
    assert api_key.status_code == 200
    assert api_key.json()["plain_text_token"].startswith("sgai_")

    integration_runtime_policy = client.patch(
        f"/api/v1/integrations/{integration_id}/runtime-policy",
        json={
            "managed_runtime_enabled": True,
            "runtime_owner": "growth-ops",
            "refresh_minutes": 240,
            "retry_backoff_minutes": [5, 30, 120],
            "token_rotation_days": 45,
            "failure_recovery_mode": "retry_then_fallback_owner",
        },
        headers=auth_headers,
    )
    assert integration_runtime_policy.status_code == 200
    assert (
        integration_runtime_policy.json()["runtime_profile"]["managed_runtime_enabled"]
        is True
    )

    evidence = client.post(
        "/api/v1/proof/evidence",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "label_type": "public_fact",
            "title": "Public before/after result",
            "summary": "Directly visible public change.",
            "source_ref": "case-study",
            "links": ["https://example.com/case"],
        },
        headers=auth_headers,
    )
    assert evidence.status_code == 200

    experiment = client.post(
        "/api/v1/proof/experiments",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "source_type": "audit_run",
            "source_id": str(audit.json()["audit_job_id"]),
            "change_summary": "Updated page structure and AI guidance files.",
            "confidence_label": "partial",
            "before_snapshot": {"score": 82},
            "after_snapshot": {"score": 86.1},
            "evidence_links": ["artifact://report/1"],
            "outcome_metrics": {"organic_clicks_delta": 12},
        },
        headers=auth_headers,
    )
    assert experiment.status_code == 200

    proof_timeline = client.get(
        f"/api/v1/proof/timeline?project_id={project_id}",
        headers=auth_headers,
    )
    assert proof_timeline.status_code == 200
    assert proof_timeline.json()["items"]

    proof_ops_center = client.get(
        f"/api/v1/settings/proof-ops-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert proof_ops_center.status_code == 200
    assert proof_ops_center.json()["summary"]["evidence_count"] >= 1

    generation_contracts = client.get(
        "/api/v1/generation/contracts", headers=auth_headers
    )
    assert generation_contracts.status_code == 200
    assert generation_contracts.json()["schema_files"]
    assert "scanner_saas" in generation_contracts.json()["project_types"]
    assert (
        generation_contracts.json()["project_generation_contract_version"] == "v6.4.0"
    )

    seo_intelligence = client.get(
        f"/api/v1/settings/seo-intelligence-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert seo_intelligence.status_code == 200
    assert seo_intelligence.json()["connected_surfaces"]
    assert seo_intelligence.json()["scorecard"]["tracked_keywords"] > 0

    generation_manifest = client.post(
        "/api/v1/generation/manifests/generate",
        json={
            "workspace_id": workspace_id,
            "project_id": project_id,
            "project_type": "scanner_saas",
            "domain_or_url": "https://example.com",
            "business_type": "legal services",
            "target_geography": "Moscow",
            "primary_stack": "wordpress",
            "required_integrations": [
                "gsc",
                "ga4",
                "google_ads",
                "yandex_webmaster",
                "yandex_metrica",
                "yandex_direct",
            ],
            "language_preference": "bilingual",
            "market_mode": "ru_market",
            "target_mode": "saas_box",
        },
        headers=auth_headers,
    )
    assert generation_manifest.status_code == 200
    assert generation_manifest.json()["manifest"]["surfaces"]

    generation_scaffold = client.post(
        f"/api/v1/generation/manifests/{generation_manifest.json()['id']}/scaffold",
        headers=auth_headers,
    )
    assert generation_scaffold.status_code == 200
    assert generation_scaffold.json()["generated_files"]
    assert any(
        item.endswith("deploy-wizard.json")
        for item in generation_scaffold.json()["generated_files"]
    )

    onboarding_center = client.get(
        "/api/v1/settings/onboarding-center", headers=auth_headers
    )
    assert onboarding_center.status_code == 200
    assert onboarding_center.json()["guided_steps"]

    one_link_builder = client.get(
        "/api/v1/settings/one-link-builder", headers=auth_headers
    )
    assert one_link_builder.status_code == 200
    assert one_link_builder.json()["recommended_prompt"]

    proof_kit = client.get("/api/v1/settings/proof-kit", headers=auth_headers)
    assert proof_kit.status_code == 200
    assert proof_kit.json()["sample_tenants"]

    social_distribution = client.get(
        "/api/v1/settings/social-distribution-center", headers=auth_headers
    )
    assert social_distribution.status_code == 200
    assert social_distribution.json()["connected_surfaces"]
    assert social_distribution.json()["useful_workflows"]

    social_intelligence = client.get(
        f"/api/v1/settings/social-intelligence-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert social_intelligence.status_code == 200
    assert social_intelligence.json()["social_modes"]
    assert social_intelligence.json()["executive_use_cases"]

    social_command = client.get(
        f"/api/v1/settings/social-command-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert social_command.status_code == 200
    assert social_command.json()["parsing_lanes"]

    social_parser = client.post(
        "/api/v1/settings/social-idea-parser",
        json={
            "project_id": project_id,
            "source": "threads",
            "raw_text": "- Why is this so expensive?\n- We saw 28% lead growth after FAQ updates.\n- Setup was slow at first.",
        },
        headers=auth_headers,
    )
    assert social_parser.status_code == 200
    assert social_parser.json()["recommended_actions"]

    repo_understanding = client.get(
        "/api/v1/settings/repo-understanding-center", headers=auth_headers
    )
    assert repo_understanding.status_code == 200
    assert repo_understanding.json()["architecture_layers"]

    deploy_wizard = client.get("/api/v1/settings/deploy-wizard", headers=auth_headers)
    assert deploy_wizard.status_code == 200
    assert deploy_wizard.json()["paths"]

    prompt_packs = client.get("/api/v1/settings/prompt-packs", headers=auth_headers)
    assert prompt_packs.status_code == 200
    assert prompt_packs.json()["packs"]

    demo_center = client.get("/api/v1/settings/demo-center", headers=auth_headers)
    assert demo_center.status_code == 200
    assert demo_center.json()["sample_projects"]

    local_entity = client.get(
        "/api/v1/settings/local-entity-center", headers=auth_headers
    )
    assert local_entity.status_code == 200
    assert local_entity.json()["google_local_stack"]

    ru_market_center = client.get(
        f"/api/v1/settings/ru-market-command-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert ru_market_center.status_code == 200
    assert "yandex_neuro" in ru_market_center.json()["connected_surfaces"]
    assert ru_market_center.json()["ru_distribution_stack"]

    productization_center = client.get(
        "/api/v1/settings/productization-center", headers=auth_headers
    )
    assert productization_center.status_code == 200
    assert productization_center.json()["billing_abstraction"]

    saas_growth_center = client.get(
        f"/api/v1/settings/saas-growth-center?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert saas_growth_center.status_code == 200
    assert saas_growth_center.json()["default_service_tiers"]

    saas_readiness_center = client.get(
        f"/api/v1/settings/saas-readiness-center?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert saas_readiness_center.status_code == 200
    assert saas_readiness_center.json()["layer_status"]
    deployment_posture = client.get(
        "/api/v1/settings/deployment-posture", headers=auth_headers
    )
    assert deployment_posture.status_code == 200
    assert deployment_posture.json()["security_posture"]

    portfolio_dashboard = client.get(
        f"/api/v1/settings/portfolio-dashboard?workspace_id={workspace_id}",
        headers=auth_headers,
    )
    assert portfolio_dashboard.status_code == 200
    assert portfolio_dashboard.json()["projects"]
    assert portfolio_dashboard.json()["workspace_breakdown"]

    org_portfolio_dashboard = client.get(
        f"/api/v1/settings/portfolio-dashboard?organization_id={organization.json()['id']}",
        headers=auth_headers,
    )
    assert org_portfolio_dashboard.status_code == 200
    assert org_portfolio_dashboard.json()["projects"]

    mention_reputation = client.get(
        f"/api/v1/settings/mention-reputation-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert mention_reputation.status_code == 200
    assert mention_reputation.json()["tracking_layers"]

    operator_board = client.get(
        f"/api/v1/settings/operator-board?project_id={project_id}",
        headers=auth_headers,
    )
    assert operator_board.status_code == 200
    assert operator_board.json()["board_columns"]
    assert operator_board.json()["summary"]["total_tasks"] >= 1

    proof_export = client.get(
        f"/api/v1/proof/export-pack?project_id={project_id}",
        headers=auth_headers,
    )
    assert proof_export.status_code == 200
    assert proof_export.json()["pdf_ready_markdown"]

    integration_health = client.get(
        f"/api/v1/integrations/health-center?project_id={project_id}",
        headers=auth_headers,
    )
    assert integration_health.status_code == 200
    assert integration_health.json()["summary"]["total_surfaces"] >= 1

    operator_center = client.get(
        "/api/v1/settings/operator-center", headers=auth_headers
    )
    assert operator_center.status_code == 200
    assert operator_center.json()["runbooks"]

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
