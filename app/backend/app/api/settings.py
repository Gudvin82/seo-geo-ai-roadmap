from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import AuditRun, CmsConnector, IntegrationConnection, ScanJob, User
from ..schemas import (
    CIGatingRead,
    ExecutiveDashboardRead,
    ManagedApiBoundaryRead,
    ProductModeRead,
    ProductModesResponse,
)
from ..services.cms import cms_contract
from ..services.integrations import integration_contract

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/repo-assets")
def repo_assets() -> dict:
    return {
        "checklists": [
            "checklists/en/technical-seo-checklist.md",
            "checklists/en/factual-consistency-checklist.md",
            "checklists/ru/technical-seo-checklist.md",
            "checklists/ru/factual-consistency-checklist.md",
        ],
        "prompts": [
            "prompts/en/ai-audit-prompt.md",
            "prompts/en/answer-ready-page-prompt.md",
            "prompts/ru/ai-audit-prompt.md",
            "prompts/ru/answer-ready-page-prompt.md",
        ],
        "templates": [
            "templates/brand-facts-template.md",
            "templates/brand-facts-template-ru.md",
            "templates/roi-model-template.md",
            "templates/roi-model-template-ru.md",
            "templates/reporting/executive-summary-v400.md",
            "templates/reporting/fix-pack-v400.md",
        ],
        "glossary": ["GLOSSARY.md", "GLOSSARY_RU.md"],
        "agents": ["AGENTS.md"],
        "extensions": [
            "extensions/vscode/",
            "extensions/chrome/",
            "integrations/telegram/bot_stub.py",
        ],
        "managed_cloud": ["infra/k8s/"],
    }


@router.get("/prompt-library")
def prompt_library() -> dict:
    return {
        "prompts": [
            {
                "id": "ai-audit-en",
                "path": "prompts/en/ai-audit-prompt.md",
                "language": "en",
                "purpose": "audit reasoning",
                "output_format": "markdown action plan",
                "model_recommendation": "claude-sonnet / gpt-4.1 / local reasoning model",
                "risk_notes": "Needs human review before publishing recommendations.",
                "human_review_required": True,
            },
            {
                "id": "answer-ready-en",
                "path": "prompts/en/answer-ready-page-prompt.md",
                "language": "en",
                "purpose": "content generation",
                "output_format": "answer-ready draft",
                "model_recommendation": "gpt-4.1 / gemini / ollama",
                "risk_notes": "Check factual claims and citations.",
                "human_review_required": True,
            },
            {
                "id": "ai-audit-ru",
                "path": "prompts/ru/ai-audit-prompt.md",
                "language": "ru",
                "purpose": "audit reasoning",
                "output_format": "markdown action plan",
                "model_recommendation": "claude-sonnet / gpt-4.1 / local reasoning model",
                "risk_notes": "Требуется human review перед публикацией.",
                "human_review_required": True,
            },
            {
                "id": "answer-ready-ru",
                "path": "prompts/ru/answer-ready-page-prompt.md",
                "language": "ru",
                "purpose": "content generation",
                "output_format": "answer-ready draft",
                "model_recommendation": "gpt-4.1 / gemini / ollama",
                "risk_notes": "Проверяйте факты и обещания бренда.",
                "human_review_required": True,
            },
        ]
    }


@router.get("/integration-starters")
def integration_starters() -> dict:
    return {
        "search_data": [
            "scripts/gsc_data_stub.py",
            "scripts/ga4_data_stub.py",
            "scripts/yandex_data_stub.py",
            "scripts/yandex_metrica_stub.py",
        ],
        "notifications": [
            "Slack webhook",
            "Telegram webhook or bot gateway",
            "Generic outgoing webhook",
        ],
        "local_llm": [
            "Ollama",
            "LocalAI",
            "vLLM-compatible OpenAI endpoint",
            "OpenAI-compatible local gateway",
        ],
    }


@router.get("/vertical-packs")
def vertical_packs() -> dict:
    return {
        "verticals": [
            {
                "id": "legal",
                "common_audits": ["factual_consistency", "entity_hierarchy_review"],
                "reporting_angle": "trust, risk, and legal proof",
            },
            {
                "id": "saas",
                "common_audits": ["llms_txt", "content_freshness", "schema_review"],
                "reporting_angle": "product discoverability and conversion clarity",
            },
            {
                "id": "local_service_business",
                "common_audits": ["local_yandex_readiness", "factual_consistency"],
                "reporting_angle": "regional proof and commercial factors",
            },
            {
                "id": "agency",
                "common_audits": ["report_pack", "patch_pack", "brand_facts"],
                "reporting_angle": "delivery consistency and client-safe outputs",
            },
            {
                "id": "expert_business",
                "common_audits": ["entity_hierarchy_review", "ai_sov_starter"],
                "reporting_angle": "founder authority and offer clarity",
            },
            {
                "id": "healthcare",
                "common_audits": ["factual_consistency", "trust_review"],
                "reporting_angle": "accuracy, safety, and YMYL guardrails",
            },
            {
                "id": "multilingual_b2b",
                "common_audits": [
                    "llms_txt",
                    "entity_hierarchy_review",
                    "international_localization",
                ],
                "reporting_angle": "cross-market positioning and factual alignment",
            },
        ]
    }


@router.get("/review-mode")
def review_mode() -> dict:
    return {
        "automatic": [
            "inventory sync",
            "starter data import",
            "artifact generation",
            "draft patch packs",
        ],
        "requires_human_review": [
            "title rewrites",
            "schema changes",
            "brand facts approval",
            "client-facing report framing",
            "human-approved publish",
        ],
        "must_not_auto_apply": [
            "silent destructive updates",
            "publish without review",
            "legal or medical claims without approval",
        ],
    }


@router.get("/product-modes", response_model=ProductModesResponse)
def product_modes() -> ProductModesResponse:
    return ProductModesResponse(
        modes=[
            ProductModeRead(
                id="repo_methodology",
                title="Repo methodology mode",
                primary_user="operator or AI agent learning the system",
                purpose="Docs, prompts, templates, command surface, and release discipline.",
                best_for=[
                    "audits",
                    "handoff",
                    "training operators",
                    "CI-gated delivery",
                ],
                first_class_paths=["README.md", "AGENTS.md", "/geo ...", "docs_site"],
                not_the_goal=["public scanner SaaS", "hidden black-box automation"],
            ),
            ProductModeRead(
                id="app_control_panel",
                title="App control panel mode",
                primary_user="team, agency, founder, or in-house operator",
                purpose="Workspace, project, provider, integration, CMS, reporting, and dashboard operations.",
                best_for=[
                    "self-hosted app usage",
                    "executive reporting",
                    "recurring audits",
                ],
                first_class_paths=[
                    "app/frontend/index.html",
                    "/api/v1/settings/executive-dashboard",
                ],
                not_the_goal=[
                    "anonymous public intake",
                    "ungoverned destructive writeback",
                ],
            ),
            ProductModeRead(
                id="scanner_intake",
                title="Scanner intake mode",
                primary_user="lead-gen or gated self-serve intake user",
                purpose="Passive or verified scanning with clear boundaries and export artifacts.",
                best_for=[
                    "client intake",
                    "lead qualification",
                    "external scan submission",
                ],
                first_class_paths=["app/frontend/scanner.html", "/api/v1/scan-jobs"],
                not_the_goal=[
                    "open crawler abuse",
                    "unsafe active scanning by default",
                ],
            ),
        ]
    )


@router.get("/ci-gating", response_model=CIGatingRead)
def ci_gating() -> CIGatingRead:
    return CIGatingRead(
        first_class_path="GitHub Actions is a first-class path for recurring audits, validation, and release gating.",
        workflows=[
            ".github/workflows/python-tests.yml",
            ".github/workflows/markdown-lint.yml",
            ".github/workflows/link-check.yml",
            ".github/workflows/script-smoke-tests.yml",
            ".github/workflows/docs-site.yml",
            ".github/workflows/security-scans.yml",
            "examples/github-actions/ai-visibility-check.yml",
        ],
        required_signals=[
            "command surface remains machine-readable",
            "integration sync contracts stay honest",
            "docs and app surfaces stay aligned",
            "scanner and app modes remain clearly separated",
        ],
        recommended_sequence=[
            "run lightweight validation on push",
            "run audit or visibility workflows on schedule",
            "attach artifacts to reports and executive dashboards",
            "re-measure via compare and drift workflows",
        ],
    )


@router.get("/managed-api-boundary", response_model=ManagedApiBoundaryRead)
def managed_api_boundary() -> ManagedApiBoundaryRead:
    return ManagedApiBoundaryRead(
        positioning=(
            "Managed/public API is a product boundary for teams that want the methodology and app surface without owning the full self-hosted runtime."
        ),
        auth_boundary=[
            "Self-hosted: workspace JWT auth plus your own infra rules.",
            "Managed: API keys or service accounts with tenant-level scoping.",
            "Public scanner paths must remain rate-limited and intentionally narrower than operator auth.",
        ],
        rate_limit_boundary=[
            "Public URL-audit intake requires conservative per-IP and per-domain throttling.",
            "Managed audit, task export, and graph endpoints should be tiered by plan and queue priority.",
        ],
        primary_resources=[
            "scanner url-audit",
            "scan job result",
            "task bundle",
            "graph snapshot",
            "executive dashboard",
        ],
        self_hosted_vs_managed={
            "self_hosted": [
                "full control over infra, models, secrets, and UI surfaces",
                "best fit for agencies, consultants, in-house teams, and custom scanner deployments",
            ],
            "managed": [
                "lighter onboarding and API consumption path",
                "narrower public contract, stronger usage controls, and clearer commercial packaging",
            ],
        },
    )


@router.get("/executive-dashboard", response_model=ExecutiveDashboardRead)
def executive_dashboard(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExecutiveDashboardRead:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project.id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    integrations = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project.id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    cms_connectors = (
        db.query(CmsConnector)
        .filter(CmsConnector.project_id == project.id)
        .order_by(CmsConnector.id.desc())
        .all()
    )
    latest_scan = (
        db.query(ScanJob)
        .filter(ScanJob.normalized_url == project.website_url)
        .order_by(ScanJob.id.desc())
        .first()
    )
    if not latest_audit:
        raise HTTPException(
            status_code=404, detail="No audit run found for executive dashboard."
        )

    findings = json.loads(latest_audit.finding_groups_json or "[]")
    priorities = [
        {
            "title": item.get("title", "Priority"),
            "priority_score": item.get("priority_score", 0),
            "recommendation": item.get("recommendation", ""),
        }
        for item in findings[:5]
    ]
    executive_score = round(float(latest_audit.summary_score or 0), 1)
    if executive_score >= 80:
        health_band = "strong"
    elif executive_score >= 60:
        health_band = "watch"
    else:
        health_band = "critical"
    return ExecutiveDashboardRead(
        project_id=project.id,
        workspace_id=project.workspace_id,
        executive_score=executive_score,
        health_band=health_band,
        narrative=(
            f"{project.name} is in {health_band} condition. "
            "Use scanner intake, structured audits, integrations, CMS review gates, and CI-backed re-measurement as one operating loop."
        ),
        metrics={
            "latest_audit_status": latest_audit.status,
            "latest_audit_mode": latest_audit.mode,
            "latest_scan_status": latest_scan.status if latest_scan else "not-run",
            "latest_scan_mode": latest_scan.scan_mode if latest_scan else "not-run",
            "selected_checks_count": len(
                json.loads(latest_audit.selected_checks_json or "[]")
            ),
            "integrations_connected": len(integrations),
            "cms_connectors_connected": len(cms_connectors),
            "product_modes": [
                "repo_methodology",
                "app_control_panel",
                "scanner_intake",
            ],
            "ci_first_class": True,
        },
        priorities=priorities,
        integrations=[
            {
                "label": row.label,
                "source_type": row.source_type,
                "status": row.last_sync_status or "created",
                "readiness_tier": integration_contract(row.source_type)[
                    "readiness_tier"
                ],
            }
            for row in integrations
        ],
        cms=[
            {
                "label": row.label,
                "cms_type": row.cms_type,
                "writeback_mode": row.writeback_mode,
                "readiness_tier": cms_contract(row.cms_type)["readiness_tier"],
            }
            for row in cms_connectors
        ],
        ci_gating=ci_gating().model_dump(),
    )
