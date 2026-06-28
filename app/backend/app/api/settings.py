from __future__ import annotations

import json
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import require_project_access, require_workspace_access
from ..config import load_settings
from ..database import get_db
from ..deps import get_current_user
from ..models import (
    AuditRun,
    CmsConnector,
    EvidenceRecord,
    ExperimentRecord,
    IntegrationConnection,
    IntegrationSyncEvent,
    NotificationEndpoint,
    Organization,
    Project,
    Report,
    ScanJob,
    SovRun,
    TenantApiKey,
    TenantProfile,
    User,
    Workspace,
    WorkspaceMembership,
)
from ..schemas import (
    CIGatingRead,
    ExecutiveDashboardRead,
    ManagedApiBoundaryRead,
    ProductModeRead,
    ProductModesResponse,
    ServiceFoundationRead,
)
from ..services.cms import cms_contract
from ..services.integrations import (
    integration_contract,
    integration_env_status,
    integration_runtime_profile,
)
from ..services.scoring import benchmark_status, ru_geo_score
from ..services.task_center import build_task_bundle_from_audit_run

router = APIRouter(prefix="/settings", tags=["settings"])


def _maturity_status(score: float) -> str:
    if score >= 0.8:
        return "strong"
    if score >= 0.55:
        return "watch"
    return "needs_work"


def _tenant_quota_alerts(row: Optional[TenantProfile]) -> list[dict]:
    if not row:
        return []
    quota = json.loads(row.quota_json or "{}")
    usage = json.loads(row.usage_json or "{}")
    alerts: list[dict] = []
    for key, limit in quota.items():
        if not isinstance(limit, (int, float)) or limit <= 0:
            continue
        used = usage.get(f"{key}_used")
        if not isinstance(used, (int, float)):
            continue
        ratio = round(float(used) / float(limit), 3)
        status = "healthy"
        if ratio >= 1:
            status = "exceeded"
        elif ratio >= 0.8:
            status = "watch"
        alerts.append(
            {
                "metric": key,
                "limit": limit,
                "used": used,
                "ratio": ratio,
                "status": status,
            }
        )
    return alerts


def _tenant_usage_health(row: Optional[TenantProfile]) -> dict:
    alerts = _tenant_quota_alerts(row)
    if not row:
        return {
            "status": "missing",
            "healthy_metrics": 0,
            "watch_metrics": 0,
            "exceeded_metrics": 0,
        }
    return {
        "status": (
            "exceeded"
            if any(item["status"] == "exceeded" for item in alerts)
            else "watch"
            if any(item["status"] == "watch" for item in alerts)
            else "healthy"
        ),
        "healthy_metrics": sum(1 for item in alerts if item["status"] == "healthy"),
        "watch_metrics": sum(1 for item in alerts if item["status"] == "watch"),
        "exceeded_metrics": sum(1 for item in alerts if item["status"] == "exceeded"),
    }


@router.get("/deployment-posture")
def deployment_posture() -> dict:
    settings_obj = load_settings()
    cors_list = settings_obj.cors_origin_list()
    uses_wildcard_cors = "*" in cors_list
    return {
        "security_posture": {
            "secret_key_mode": (
                "ephemeral_generated"
                if settings_obj.secret_key_is_ephemeral
                else "explicit"
            ),
            "cors_mode": "wildcard" if uses_wildcard_cors else "restricted_list",
            "auto_create_schema": settings_obj.auto_create_schema,
            "auto_create_schema_mode": settings_obj.auto_create_schema_mode,
            "database_url_kind": (
                "sqlite"
                if settings_obj.database_url.startswith("sqlite:///")
                else "external"
            ),
        },
        "recommended_production_actions": [
            "set APP_SECRET_KEY explicitly in production",
            "set APP_CORS_ORIGINS to explicit trusted domains only",
            "set APP_AUTO_CREATE_SCHEMA=false once migrations are established",
            "keep public scanner flags disabled unless governance and rate limits are intentional",
        ],
        "current_flags": {
            "allow_public_intake": settings_obj.allow_public_intake,
            "allow_active_scan": settings_obj.allow_active_scan,
            "allow_anonymous_submission": settings_obj.allow_anonymous_submission,
            "allow_full_scan": settings_obj.allow_full_scan,
        },
    }


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
        "tooling_boosters": [
            "scripts/checklist_generator.py",
            "scripts/semantic_gap_mapper.py",
            "scripts/proof_pack_builder.py",
            "scripts/case_library_builder.py",
            "scripts/synthetic_case_builder.py",
            "scripts/issue_pack_generator.py",
            "examples/semantic-keywords-example.txt",
        ],
        "glossary": ["GLOSSARY.md", "GLOSSARY_RU.md"],
        "agents": ["AGENTS.md"],
        "positioning": [
            "WHAT_THIS_PROJECT_IS.md",
            "WHAT_THIS_PROJECT_IS_NOT.md",
            "WHAT_THIS_PROJECT_IS_RU.md",
            "WHAT_THIS_PROJECT_IS_NOT_RU.md",
        ],
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


@router.get("/docs-consolidation-center")
def docs_consolidation_center() -> dict:
    return {
        "current_entrypoints": [
            "README.md",
            "README_RU.md",
            "DOCS_INDEX.md",
            "DOCS_INDEX_RU.md",
            "METHODOLOGY.md",
            "METHODOLOGY_RU.md",
            "PUBLIC_PRODUCT_READINESS.md",
            "PUBLIC_PRODUCT_READINESS_RU.md",
        ],
        "operator_paths": {
            "human_operator": ["WALKTHROUGH.md", "WALKTHROUGH_RU.md"],
            "ai_agent": ["START_HERE_FOR_AI.md", "START_HERE_FOR_AI_RU.md"],
            "service_builder": [
                "ONE_DAY_SERVICE_BLUEPRINT.md",
                "ONE_DAY_SERVICE_BLUEPRINT_RU.md",
            ],
        },
        "archive_policy": {
            "current_docs_first": True,
            "historical_release_notes_in_archive": True,
            "historical_paths": [
                "DOCS_ARCHIVE.md",
                "DOCS_ARCHIVE_RU.md",
                "CHANGELOG.md",
            ],
        },
        "recommended_cleanup_rules": [
            "treat README, DOCS_INDEX, METHODOLOGY, and PUBLIC_PRODUCT_READINESS as the live root path",
            "treat versioned release docs as proof and historical slices, not the main explanation path",
            "promote repeat-used release lessons into current root docs instead of cloning more one-off docs",
        ],
    }


@router.get("/managed-integration-center")
def managed_integration_center() -> dict:
    priority_sources = [
        "gsc",
        "ga4",
        "google_ads",
        "yandex_webmaster",
        "yandex_metrica",
        "yandex_direct",
        "google_business_profile",
        "yandex_business",
        "alice_ai_visibility",
        "crux",
    ]
    rows = []
    for source_type in priority_sources:
        contract = integration_contract(source_type)
        env_status = integration_env_status(contract)
        runtime_profile = integration_runtime_profile(
            source_type,
            config={"managed_runtime_enabled": True, "refresh_minutes": 1440},
        )
        rows.append(
            {
                "source_type": source_type,
                "label": contract["label"],
                "readiness_tier": contract["readiness_tier"],
                "runtime_level": runtime_profile["runtime_level"],
                "credential_ready": runtime_profile["credential_ready"],
                "required_env_vars": env_status["required_env_vars"],
                "missing_env_vars": env_status["missing_env_vars"],
                "sync_mode": contract["sync_mode"],
                "production_flow": contract["production_flow"],
                "ci_gates": contract["ci_gates"],
                "capabilities": contract["capabilities"],
                "next_step": contract["next_step"],
            }
        )
    return {
        "summary": {
            "first_class_integrations": len(rows),
            "credential_ready_count": len(
                [row for row in rows if row["credential_ready"]]
            ),
            "runtime_ready_count": len(
                [row for row in rows if row["runtime_level"] == "managed_runtime"]
            ),
        },
        "rows": rows,
        "operator_rule": (
            "Treat GSC, GA4, Ads, Yandex, local business, Alice AI, and CrUX as "
            "one managed operating layer with credential lifecycle, refresh "
            "cadence, CI gates, and explicit recovery ownership."
        ),
    }


@router.get("/integration-starters")
def integration_starters() -> dict:
    return {
        "search_data": [
            "scripts/gsc_data_stub.py",
            "scripts/ga4_data_stub.py",
            "scripts/google_ads_stub.py",
            "scripts/yandex_data_stub.py",
            "scripts/yandex_metrica_stub.py",
            "scripts/yandex_direct_stub.py",
            "scripts/indexnow_stub.py",
            "scripts/google_business_profile_stub.py",
            "scripts/yandex_business_stub.py",
            "scripts/merchant_center_stub.py",
            "scripts/meta_ads_stub.py",
            "scripts/x_ads_stub.py",
            "scripts/x_organic_stub.py",
            "scripts/threads_stub.py",
            "scripts/reddit_mentions_stub.py",
            "scripts/tiktok_organic_stub.py",
            "scripts/vk_ads_stub.py",
            "scripts/telegram_ads_stub.py",
            "scripts/alice_ai_visibility_stub.py",
            "scripts/youtube_analytics_stub.py",
            "scripts/linkedin_ads_stub.py",
            "scripts/instagram_facebook_organic_stub.py",
        ],
        "seo_intelligence": [
            "scripts/keyword_research_stub.py",
            "scripts/competitor_intelligence_stub.py",
            "scripts/backlink_intelligence_stub.py",
            "scripts/rank_tracking_stub.py",
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


@router.get("/onboarding-center")
def onboarding_center() -> dict:
    return {
        "guided_steps": [
            "create organization or workspace",
            "create tenant profile",
            "connect one provider",
            "connect core integrations",
            "run first audit",
            "verify executive dashboard",
            "generate handoff or build manifest",
        ],
        "environment_validator": [
            "API base configured",
            "database reachable",
            "provider secrets present",
            "integration secrets present",
            "scanner mode boundaries confirmed",
        ],
        "troubleshooting_paths": [
            "provider auth mismatch",
            "integration credential missing",
            "scanner ownership verification blocked",
            "sync freshness stale",
            "dashboard waiting on first audit",
        ],
    }


@router.get("/operator-center")
def operator_center() -> dict:
    return {
        "runbooks": [
            "first-day operator runbook",
            "weekly executive review",
            "integration failure triage",
            "scanner queue review",
            "client handoff pack",
        ],
        "agency_playbooks": [
            "multi-client workspace setup",
            "white-label reporting path",
            "issue-to-patch-to-remeasure loop",
        ],
        "cost_governance": [
            "prefer one hosted provider plus one local fallback",
            "run expensive checks on schedule, not on every click",
            "separate core search truth from supporting social context",
        ],
    }


@router.get("/one-link-builder")
def one_link_builder() -> dict:
    return {
        "promise": "Give one link and one prompt to an AI agent, then deploy a working SEO/GEO/AI operating workspace faster.",
        "required_inputs": [
            "domain_or_url",
            "business_type",
            "target_geography",
            "language_preference",
            "target_mode",
        ],
        "recommended_prompt": (
            "Use this repository as the platform contract. Build the generated project, "
            "connect the requested integrations, scaffold the scanner, admin, dashboard, "
            "proof layer, and return deployment plus first-audit instructions."
        ),
        "deploy_paths": [
            "local docker demo",
            "self-hosted VPS docker compose",
            "managed deployment starter",
            "saas box mode starter",
        ],
        "first_class_docs": [
            "BUILD_WITH_THIS_PLATFORM.md",
            "GENERATE_PROJECT_FROM_URL.md",
            "START_HERE_FOR_AI.md",
        ],
    }


@router.get("/proof-kit")
def proof_kit() -> dict:
    return {
        "labels": [
            "public_fact",
            "bounded_rollout_record",
            "internal_evidence",
            "demo_fixture",
            "synthetic_example",
        ],
        "sample_tenants": [
            {
                "tenant_name": "Local service starter",
                "plan_code": "starter",
                "project_type": "local_business",
                "suggested_integrations": [
                    "gsc",
                    "ga4",
                    "google_business_profile",
                    "crux",
                ],
            },
            {
                "tenant_name": "RU growth workspace",
                "plan_code": "growth",
                "project_type": "agency_client_workspace",
                "suggested_integrations": [
                    "yandex_webmaster",
                    "yandex_metrica",
                    "yandex_direct",
                    "yandex_business",
                ],
            },
        ],
        "benchmark_fixtures": {
            "ai_visibility_target": "0.20+ share for priority branded prompts",
            "field_performance_target": "LCP p75 under 2500 ms",
            "local_trust_target": "4.7+ average rating with active review flow",
        },
        "evidence_packs": [
            "before_after_metric_pack",
            "executive_summary_sample",
            "client_delivery_sample",
            "experiment_log_sample",
            "issue_pack_sample",
            "synthetic_case_sample",
            "case_library_index_sample",
        ],
        "proof_workflows": [
            "public bounded case",
            "synthetic training case",
            "issue-pack handoff",
            "client-safe proof export",
        ],
    }


@router.get("/social-distribution-center")
def social_distribution_center() -> dict:
    return {
        "connected_surfaces": [
            "meta_ads",
            "x_ads",
            "x_organic",
            "threads",
            "reddit_mentions",
            "tiktok_organic",
            "vk_ads",
            "vk_organic",
            "telegram_ads",
            "telegram_channels",
            "dzen",
            "rutube",
            "youtube",
            "linkedin_ads",
            "instagram_facebook_organic",
            "google_business_profile",
            "yandex_business",
        ],
        "priority_expansions": [
            "brand mention tracking",
            "reputation event timeline",
            "community demand comparison",
            "local-business trust overlays",
            "social content opportunity queue",
            "founder-led thought leadership parsing",
            "comment-to-faq extraction",
            "RU-native social demand overlays",
            "community-to-sales narrative packs",
        ],
        "mention_tracking_model": {
            "starter_mode": "track mentions through evidence records and operator notes",
            "next_mode": "connect external social monitoring or API-backed ingestion",
        },
        "useful_workflows": [
            "parse best posts into FAQ and answer-ready pages",
            "turn repeated social questions into landing-page objections",
            "map community mentions to executive narrative and proof packs",
            "compare social amplification with branded search and AI citations",
            "compare RU community demand with Yandex search and local trust signals",
            "turn Telegram and VK conversations into operator-ready sales angles",
        ],
    }


@router.get("/social-intelligence-center")
def social_intelligence_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    snapshots = {
        row.source_type: json.loads(row.latest_snapshot_json or "{}")
        for row in integration_rows
    }
    supported_surfaces = [
        "meta_ads",
        "x_ads",
        "x_organic",
        "threads",
        "reddit_mentions",
        "tiktok_organic",
        "vk_ads",
        "vk_organic",
        "telegram_ads",
        "telegram_channels",
        "dzen",
        "rutube",
        "youtube",
        "linkedin_ads",
        "instagram_facebook_organic",
    ]
    connected = [surface for surface in supported_surfaces if surface in snapshots]
    opportunity_queue: list[dict[str, str]] = []
    for surface in [
        "x_organic",
        "threads",
        "reddit_mentions",
        "tiktok_organic",
        "vk_organic",
        "telegram_channels",
        "dzen",
    ]:
        snapshot = snapshots.get(surface) or {}
        for idea in snapshot.get("opportunities", [])[:2]:
            opportunity_queue.append(
                {
                    "surface": surface,
                    "type": "content_opportunity",
                    "action": idea,
                }
            )

    comparison = {
        "supporting_social_clicks": sum(
            float(
                (snapshots.get(surface, {}).get("metrics") or {}).get("site_clicks", 0)
            )
            for surface in supported_surfaces
        ),
        "supporting_social_leads": sum(
            float((snapshots.get(surface, {}).get("metrics") or {}).get("leads", 0))
            for surface in supported_surfaces
        ),
        "supporting_social_mentions": sum(
            float((snapshots.get(surface, {}).get("metrics") or {}).get("mentions", 0))
            for surface in supported_surfaces
        ),
    }
    return {
        "project_id": project.id,
        "project_name": project.name,
        "connected_surfaces": connected,
        "social_modes": [
            "amplification",
            "community demand",
            "reputation sensing",
            "content opportunity parsing",
            "RU community mining",
            "local-business proof extraction",
        ],
        "opportunity_queue": opportunity_queue,
        "executive_use_cases": [
            "feed social questions into GEO content planning",
            "link amplification data to brand demand and AI visibility",
            "turn positive community proof into client-safe deliverables",
            "compare RU social demand against Yandex demand and local actions",
        ],
        "comparison": comparison,
    }


@router.get("/social-command-center")
def social_command_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    snapshots = {
        row.source_type: json.loads(row.latest_snapshot_json or "{}")
        for row in integration_rows
    }
    social_sources = [
        "meta_ads",
        "x_ads",
        "x_organic",
        "threads",
        "reddit_mentions",
        "tiktok_organic",
        "vk_ads",
        "vk_organic",
        "telegram_ads",
        "telegram_channels",
        "dzen",
        "rutube",
        "youtube",
        "linkedin_ads",
        "instagram_facebook_organic",
    ]
    connected = [item for item in social_sources if item in snapshots]
    backlog: list[dict[str, str]] = []
    for source in connected:
        snapshot = snapshots.get(source) or {}
        for item in snapshot.get("opportunities", [])[:3]:
            backlog.append(
                {
                    "source": source,
                    "item_type": "content_opportunity",
                    "action": item,
                }
            )
    return {
        "project_id": project.id,
        "project_name": project.name,
        "connected_surfaces": connected,
        "parsing_lanes": [
            "comments to FAQ",
            "mentions to proof blocks",
            "threads to landing-page objections",
            "short-form hooks to title and CTA tests",
            "VK and Telegram community language to RU sales copy",
            "local-business review signals to trust blocks",
        ],
        "operator_loops": [
            "capture social demand",
            "convert recurring questions into answer-ready content",
            "route proof into executive and client-safe exports",
            "compare supporting social demand with branded search and AI visibility",
            "tie RU community demand to Yandex demand and local-business entities",
        ],
        "backlog": backlog,
        "ready_assets": [
            "faq_page",
            "landing_objection_block",
            "proof_strip",
            "founder_thought_leadership_page",
            "ru_market_trust_block",
            "community-proof carousel",
        ],
    }


@router.post("/social-idea-parser")
def social_idea_parser(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project_id = payload.get("project_id")
    if project_id is not None:
        require_project_access(db, int(project_id), current_user, minimum_role="viewer")
    source = str(payload.get("source") or "social").strip().lower()
    raw_text = str(payload.get("raw_text") or "").strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="raw_text is required.")
    lines = [line.strip("- ").strip() for line in raw_text.splitlines() if line.strip()]
    lowered = [line.lower() for line in lines]
    questions = [line for line in lines if "?" in line]
    objections = [
        line
        for line, lower in zip(lines, lowered)
        if any(
            token in lower
            for token in [
                "дорого",
                "expensive",
                "сложно",
                "hard",
                "непонят",
                "unclear",
                "долго",
                "slow",
            ]
        )
    ]
    proof_points = [
        line
        for line, lower in zip(lines, lowered)
        if any(
            token in lower
            for token in [
                "result",
                "growth",
                "lift",
                "case",
                "кейс",
                "рост",
                "%",
                "leads",
                "traffic",
            ]
        )
    ]
    pain_points = [
        line
        for line, lower in zip(lines, lowered)
        if any(
            token in lower
            for token in [
                "problem",
                "issue",
                "pain",
                "ошиб",
                "проблем",
                "не работает",
                "does not work",
            ]
        )
    ]
    actions = []
    if questions:
        actions.append("create or expand a visible FAQ block from repeated questions")
    if objections:
        actions.append("add objection-handling copy to the landing or service page")
    if proof_points:
        actions.append(
            "turn proof points into case-study or testimonial evidence blocks"
        )
    if pain_points:
        actions.append(
            "map pain points into audit offer messaging and answer-ready pages"
        )
    if not actions:
        actions.append(
            "summarize the social thread into a short operator brief and test one new content angle"
        )
    return {
        "source": source,
        "raw_line_count": len(lines),
        "questions": questions,
        "objections": objections,
        "proof_points": proof_points,
        "pain_points": pain_points,
        "recommended_assets": [
            "faq_page",
            "landing_objection_block",
            "proof_strip",
            "executive_summary_note",
        ],
        "recommended_actions": actions,
        "client_safe_summary": (
            f"Parsed {len(lines)} social signal lines from {source}. "
            f"Found {len(questions)} questions, {len(objections)} objections, "
            f"{len(proof_points)} proof points, and {len(pain_points)} pain points."
        ),
    }


@router.get("/saas-growth-center")
def saas_growth_center(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    projects = (
        db.query(Project)
        .filter(Project.workspace_id == workspace_id)
        .order_by(Project.id.asc())
        .all()
    )
    return {
        "workspace_id": workspace_id,
        "client_surfaces": [
            "executive dashboard",
            "client-safe proof exports",
            "scanner intake",
            "operator board",
            "integration health center",
            "social intelligence center",
        ],
        "growth_loops": [
            "audit -> proof -> client report -> fix -> rerun",
            "social question -> FAQ -> landing update -> citation lift",
            "campaign demand -> search demand -> conversion narrative",
        ],
        "default_service_tiers": [
            {
                "tier": "starter",
                "best_for": "one brand or solo operator",
                "includes": ["scanner", "audits", "proof", "basic social intelligence"],
            },
            {
                "tier": "agency",
                "best_for": "multi-client workspace",
                "includes": [
                    "portfolio view",
                    "client-safe exports",
                    "operator board",
                    "integration health",
                ],
            },
            {
                "tier": "growth",
                "best_for": "teams that need search + social + AI operating center",
                "includes": [
                    "executive overlays",
                    "social opportunity queue",
                    "SaaS governance surfaces",
                ],
            },
        ],
        "project_count": len(projects),
        "service_promises": [
            "self-hosted by default",
            "AI-agent deployable",
            "client-report ready",
            "search + GEO + social intelligence in one operating layer",
        ],
    }


@router.get("/saas-readiness-center")
def saas_readiness_center(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    workspace, membership = require_workspace_access(
        db, workspace_id, current_user, minimum_role="viewer"
    )
    tenant = (
        db.query(TenantProfile)
        .filter(TenantProfile.workspace_id == workspace_id)
        .order_by(TenantProfile.id.desc())
        .first()
    )
    tenant_keys = (
        db.query(TenantApiKey).filter(TenantApiKey.workspace_id == workspace_id).count()
    )
    notification_count = (
        db.query(NotificationEndpoint)
        .filter(NotificationEndpoint.workspace_id == workspace_id)
        .count()
    )
    layer_status = {
        "auth_and_rbac": "ready",
        "tenant_profile": "ready" if tenant else "missing",
        "quota_and_usage": "ready"
        if tenant and json.loads(tenant.quota_json or "{}")
        else "needs_operator_policy",
        "tenant_api_keys": "ready" if tenant_keys else "missing",
        "notification_ops": "ready" if notification_count else "needs_setup",
        "public_scanner_guardrails": "operator_ready",
        "durable_queue": "foundation_ready_but_not_managed",
        "billing": "intentionally_not_required_free_project",
        "hosted_domain": "intentionally_out_of_scope_for_this_release",
    }
    readiness_score = 0
    for value in layer_status.values():
        if value == "ready":
            readiness_score += 14
        elif value == "operator_ready":
            readiness_score += 10
        elif value == "foundation_ready_but_not_managed":
            readiness_score += 8
    return {
        "workspace_id": workspace.id,
        "workspace_slug": workspace.slug,
        "role": membership.role,
        "readiness_score": readiness_score,
        "layer_status": layer_status,
        "safe_announcement": (
            "self-hosted SaaS-ready platform"
            if readiness_score >= 60
            else "strong SaaS foundation"
        ),
        "still_needed_for_full_managed_saas": [
            "maintainer-hosted runtime",
            "enterprise SSO or SCIM",
        ],
        "operator_next_steps": [
            "connect at least two providers with one local fallback",
            "create one tenant profile and one tenant API key",
            "configure at least one notification endpoint",
            "run scanner, audit, proof export, and executive refresh on one project",
            "treat billing as optional because the project is intentionally free and self-hosted",
        ],
    }


@router.get("/repo-understanding-center")
def repo_understanding_center() -> dict:
    return {
        "positioning": (
            "This mode helps an AI or human operator understand the repository "
            "fast enough to deploy, extend, and govern it without reading every file."
        ),
        "modes": [
            {
                "id": "methodology",
                "question": "Where is the SEO/GEO/AI methodology?",
                "entrypoints": [
                    "README.md",
                    "README_RU.md",
                    "docs/en/",
                    "docs/ru/",
                    "WALKTHROUGH.md",
                ],
            },
            {
                "id": "app_runtime",
                "question": "Where is the working product surface?",
                "entrypoints": [
                    "app/backend/app/main.py",
                    "app/backend/app/api/",
                    "app/frontend/index.html",
                    "app/frontend/scanner.html",
                ],
            },
            {
                "id": "graph_intelligence",
                "question": "How do graph and explainability surfaces work?",
                "entrypoints": [
                    "app/backend/app/api/graph_runtime.py",
                    "app/backend/app/services/graph_runtime.py",
                    "app/frontend/graph.html",
                ],
            },
            {
                "id": "ai_to_app",
                "question": "How does AI-to-App generation work?",
                "entrypoints": [
                    "app/backend/app/api/generation.py",
                    "contracts/project-blueprint.schema.json",
                    "BUILD_WITH_THIS_PLATFORM.md",
                    "GENERATE_PROJECT_FROM_URL.md",
                ],
            },
        ],
        "architecture_layers": [
            {
                "name": "control_plane",
                "why_it_exists": "workspace, project, auth, governance, reporting",
                "core_paths": [
                    "app/backend/app/api/",
                    "app/backend/app/models.py",
                    "app/backend/app/schemas.py",
                ],
            },
            {
                "name": "scanner_and_audit_plane",
                "why_it_exists": "scan jobs, audits, findings, exports, proof",
                "core_paths": [
                    "app/backend/app/services/scan_jobs.py",
                    "app/backend/app/services/audits.py",
                    "app/backend/app/api/proof.py",
                    "app/backend/app/api/task_center.py",
                ],
            },
            {
                "name": "integration_plane",
                "why_it_exists": "provider and external data sync contracts",
                "core_paths": [
                    "app/backend/app/api/integrations.py",
                    "app/backend/app/services/integrations.py",
                    "scripts/",
                ],
            },
            {
                "name": "operator_ui",
                "why_it_exists": "daily operating system for teams and AI agents",
                "core_paths": [
                    "app/frontend/index.html",
                    "app/frontend/app.js",
                    "app/frontend/graph.html",
                ],
            },
        ],
        "fastest_questions_for_ai": [
            "What are the main product modes?",
            "Which endpoints create the first working audit loop?",
            "Which files define contracts and machine-readable outputs?",
            "Which UI pages are operator-first versus public-intake?",
            "What can be deployed immediately and what is still starter-level?",
        ],
        "recommended_handoff_prompt": (
            "Understand this repository as a self-hosted SEO/GEO/AI operating system. "
            "Map the product modes, identify the shortest deploy path, explain the "
            "architecture in plain English, then execute the requested deployment or audit."
        ),
    }


@router.get("/deploy-wizard")
def deploy_wizard() -> dict:
    return {
        "promise": "Choose one runtime path and get a concrete operator-grade deployment sequence.",
        "paths": [
            {
                "id": "local",
                "label": "Local",
                "best_for": "15-minute demo, UI walkthrough, first AI handoff",
                "steps": [
                    "copy .env.example",
                    "run make up",
                    "run make migrate",
                    "run make demo",
                    "open app and scanner pages",
                ],
                "verification": [
                    "login works",
                    "demo tenant exists",
                    "first audit can run",
                ],
            },
            {
                "id": "vps_docker",
                "label": "VPS Docker",
                "best_for": "serious self-hosted usage on your own server",
                "steps": [
                    "prepare DNS and reverse proxy",
                    "copy production env",
                    "run docker compose up -d",
                    "run migrations",
                    "configure backups and secrets",
                ],
                "verification": ["health endpoint ok", "auth ok", "background jobs ok"],
            },
            {
                "id": "coolify",
                "label": "Coolify",
                "best_for": "self-hosted platform teams that want managed deployment UX",
                "steps": [
                    "import repository into Coolify",
                    "set env vars and persistent services",
                    "deploy web and worker surfaces",
                    "run post-deploy migrations",
                ],
                "verification": [
                    "web deploy ok",
                    "worker connectivity ok",
                    "storage paths ok",
                ],
            },
            {
                "id": "railway",
                "label": "Railway",
                "best_for": "fast hosted app setup with moderate ops friction",
                "steps": [
                    "connect repo",
                    "provision Postgres",
                    "set secrets",
                    "deploy app",
                    "verify scheduled and sync flows",
                ],
                "verification": [
                    "database ok",
                    "first login ok",
                    "integration sync ok",
                ],
            },
            {
                "id": "render",
                "label": "Render",
                "best_for": "managed web service deployment with explicit services",
                "steps": [
                    "create web service and database",
                    "set build and start commands",
                    "apply env",
                    "run migrations",
                ],
                "verification": [
                    "service healthy",
                    "scanner page reachable",
                    "reports writable",
                ],
            },
            {
                "id": "kubernetes",
                "label": "Kubernetes",
                "best_for": "larger agency or platform teams",
                "steps": [
                    "use infra/k8s manifests as starter",
                    "bind secrets and ingress",
                    "deploy web plus worker surfaces",
                    "configure horizontal scaling and storage",
                ],
                "verification": [
                    "rollout healthy",
                    "logs centralized",
                    "queue and storage stable",
                ],
            },
        ],
        "operator_rule": "Start with the smallest path that proves value, then harden.",
    }


@router.get("/prompt-packs")
def prompt_packs() -> dict:
    return {
        "packs": [
            {
                "id": "deploy-for-me",
                "label": "Deploy for me",
                "prompt": (
                    "Use this repository as the deployment contract. Stand up the app, "
                    "configure env, run migrations, prepare demo access, and verify the UI."
                ),
            },
            {
                "id": "audit-my-site",
                "label": "Audit my site",
                "prompt": (
                    "Use this repository methodology and runtime. Audit my site, collect "
                    "SEO/GEO/AI findings, generate proof, and return an executive summary."
                ),
            },
            {
                "id": "generate-client-scanner",
                "label": "Generate client scanner",
                "prompt": (
                    "Generate a client-facing scanner service from this repository, keeping "
                    "operator governance, public-intake boundaries, and export artifacts."
                ),
            },
            {
                "id": "fix-and-rerun",
                "label": "Fix and rerun",
                "prompt": (
                    "Use the latest findings, prepare a safe fix plan, apply only approved "
                    "changes, then rerun audits and compare proof deltas."
                ),
            },
        ],
        "usage_rule": "These are starter prompts. The repo contracts and UI still define the source of truth.",
    }


@router.get("/demo-center")
def demo_center() -> dict:
    return {
        "public_demo_tenant": {
            "name": "Discoverability OS Demo Tenant",
            "access_mode": "local demo credentials or self-hosted sample fixture",
            "recommended_entrypoints": [
                "app/frontend/index.html",
                "app/frontend/scanner.html",
                "app/frontend/graph.html",
            ],
        },
        "sample_projects": [
            {
                "name": "Local business sample",
                "project_type": "local_business_dashboard",
                "why_it_matters": "best for Google/Yandex local SEO and maps signals",
            },
            {
                "name": "Agency scanner sample",
                "project_type": "scanner_saas",
                "why_it_matters": "best for public intake and white-label audit delivery",
            },
            {
                "name": "E-commerce ops sample",
                "project_type": "ecommerce_ops",
                "why_it_matters": "best for Merchant Center, performance, and revenue overlays",
            },
        ],
        "demo_fixtures": [
            "sample tenant profile",
            "sample executive dashboard",
            "sample proof timeline",
            "sample AI-to-App manifest",
        ],
    }


@router.get("/local-entity-center")
def local_entity_center() -> dict:
    return {
        "google_local_stack": [
            "Google Business Profile completeness",
            "review volume and rating trend",
            "entity consistency across landing pages and profile",
            "location-to-landing-page alignment",
            "maps actions and local conversion overlays",
        ],
        "yandex_local_stack": [
            "Yandex Business completeness",
            "Yandex Webmaster regional readiness",
            "YandexAdditional and RU AI bot discoverability",
            "Yandex Neuro readiness and trust overlays",
            "local trust and legal blocks for RU market",
            "RU snippets and answer-ready content",
        ],
        "entity_requirements": [
            "clear legal/business identity",
            "address and contact consistency",
            "service area or region clarity",
            "structured data and trust blocks",
            "FAQ and answer-ready content for local intent",
        ],
        "ru_growth_extensions": [
            "VK community proof loops",
            "Telegram channel demand overlays",
            "Yandex Direct + Metrica + Business local attribution",
            "2GIS-style local trust packaging in deliverables",
        ],
    }


@router.get("/ru-market-command-center")
def ru_market_command_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    snapshots = {
        row.source_type: json.loads(row.latest_snapshot_json or "{}")
        for row in integration_rows
    }
    ru_stack = [
        "yandex_webmaster",
        "yandex_metrica",
        "yandex_direct",
        "yandex_business",
        "yandex_neuro",
        "vk_ads",
        "vk_organic",
        "telegram_ads",
        "telegram_channels",
        "dzen",
        "rutube",
    ]
    connected = [surface for surface in ru_stack if surface in snapshots]
    source_rows = []
    for row in integration_rows:
        if row.source_type not in ru_stack:
            continue
        snapshot = json.loads(row.latest_snapshot_json or "{}")
        source_rows.append(
            {
                "source_type": row.source_type,
                "label": row.label,
                "runtime_profile": integration_runtime_profile(
                    row.source_type,
                    config=json.loads(row.config_json or "{}"),
                    credentials_env_var=row.credentials_env_var,
                    latest_snapshot=snapshot,
                ),
                "latest_snapshot_source": snapshot.get("source"),
                "metrics": snapshot.get("metrics", {}),
            }
        )
    return {
        "project_id": project.id,
        "project_name": project.name,
        "connected_surfaces": connected,
        "ru_search_stack": [
            "Yandex Webmaster",
            "Yandex Metrica",
            "Yandex Direct",
            "Yandex Business",
            "YandexAdditional / Neuro readiness",
        ],
        "ru_distribution_stack": [
            "VK Ads",
            "VK Organic",
            "Telegram Ads",
            "Telegram Channels",
            "Dzen",
            "RuTube",
        ],
        "ru_local_stack": [
            "Yandex Business trust and action metrics",
            "regional landing-page alignment",
            "legal and trust blocks for service pages",
            "review and reputation overlays",
        ],
        "operator_plays": [
            "compare Yandex demand with VK and Telegram community demand",
            "turn RU objections into trust and FAQ blocks",
            "pair Yandex Business proof with local landing-page conversions",
            "treat YandexAdditional access and answer-ready content as a first-class GEO signal",
        ],
        "channel_comparison": {
            "paid_sources": ["yandex_direct", "vk_ads", "telegram_ads"],
            "community_sources": ["vk_organic", "telegram_channels", "dzen"],
            "video_sources": ["rutube", "youtube"],
            "local_sources": ["yandex_business", "google_business_profile"],
        },
        "source_rows": source_rows,
    }


@router.get("/productization-center")
def productization_center() -> dict:
    return {
        "billing_abstraction": [
            "workspace plan code",
            "usage and quota policy",
            "manual invoice or Stripe-assisted path",
        ],
        "sso_starter": [
            "reverse proxy auth header mode",
            "OIDC gateway starter",
            "hosted IdP planning layer",
        ],
        "tenant_admin_console": [
            "organization catalog",
            "tenant overview",
            "workspace API keys",
            "quota and usage visibility",
        ],
        "hosted_tier_boundary": [
            "narrower public API than self-hosted",
            "rate-limited public scanner",
            "queue priority by plan",
            "proof-safe exports only",
        ],
    }


@router.get("/tenant-admin-console")
def tenant_admin_console(
    workspace_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    if workspace_id:
        require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
        workspace_ids = [workspace_id]
    else:
        workspace_ids = [
            row.id
            for row in db.query(Workspace)
            .filter(Workspace.owner_user_id == current_user.id)
            .order_by(Workspace.id.asc())
            .all()
        ]
    tenant_rows_query = db.query(TenantProfile).filter(
        TenantProfile.workspace_id.in_(workspace_ids or [0])
    )
    if organization_id is not None:
        tenant_rows_query = tenant_rows_query.filter(
            TenantProfile.organization_id == organization_id
        )
    tenant_rows = tenant_rows_query.order_by(TenantProfile.id.desc()).all()
    org_map = {
        row.id: row
        for row in db.query(Organization)
        .filter(Organization.owner_user_id == current_user.id)
        .all()
    }
    api_keys = (
        db.query(TenantApiKey)
        .filter(TenantApiKey.workspace_id.in_(workspace_ids or [0]))
        .order_by(TenantApiKey.id.desc())
        .all()
    )
    api_keys_by_workspace: dict[int, list[TenantApiKey]] = {}
    for row in api_keys:
        api_keys_by_workspace.setdefault(row.workspace_id, []).append(row)
    tenants = []
    for row in tenant_rows:
        org = org_map.get(row.organization_id)
        key_rows = api_keys_by_workspace.get(row.workspace_id, [])
        quota = json.loads(row.quota_json or "{}")
        usage = json.loads(row.usage_json or "{}")
        onboarding = json.loads(row.onboarding_state_json or "{}")
        tenants.append(
            {
                "tenant_profile_id": row.id,
                "workspace_id": row.workspace_id,
                "organization_id": row.organization_id,
                "organization_name": org.name if org else None,
                "tenant_name": row.tenant_name,
                "plan_code": row.plan_code,
                "plan_status": row.plan_status,
                "quota": quota,
                "usage": usage,
                "usage_health": _tenant_usage_health(row),
                "onboarding_state": onboarding,
                "api_key_count": len(key_rows),
                "enabled_api_key_count": len(
                    [item for item in key_rows if item.is_enabled]
                ),
            }
        )
    return {
        "summary": {
            "organization_count": len(org_map),
            "workspace_count": len(workspace_ids),
            "tenant_count": len(tenant_rows),
            "api_key_count": len(api_keys),
            "enabled_api_key_count": len([row for row in api_keys if row.is_enabled]),
        },
        "filters": {
            "workspace_id": workspace_id,
            "organization_id": organization_id,
        },
        "tenants": tenants,
        "recommended_operator_actions": [
            "review usage and quota pressure before adding new client workloads",
            "disable stale tenant API keys and rotate short-lived credentials",
            "keep onboarding states explicit so service delivery does not hide partial setup",
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
                first_class_paths=[
                    "README.md",
                    "METHODOLOGY.md",
                    "SCORING_EXPLAINED.md",
                    "AI_TASK_PACKS.md",
                    "AGENTS.md",
                    "/geo ...",
                    "docs_site",
                ],
                not_the_goal=["public scanner SaaS", "hidden black-box automation"],
            ),
            ProductModeRead(
                id="seo_intelligence_lab",
                title="SEO intelligence lab mode",
                primary_user="growth, SEO, or content strategy operator",
                purpose="Keyword demand, competitor gaps, authority shifts, and rank visibility in one operator loop.",
                best_for=[
                    "keyword strategy",
                    "competitor benchmarking",
                    "authority recovery",
                    "rank visibility review",
                ],
                first_class_paths=[
                    "/api/v1/settings/seo-intelligence-center",
                    "/api/v1/integrations/health-center",
                    "scripts/keyword_research_stub.py",
                ],
                not_the_goal=[
                    "hidden third-party data dependency",
                    "black-box SEO score with no evidence",
                ],
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
            ProductModeRead(
                id="service_builder",
                title="Service builder mode",
                primary_user="team turning the repo into a branded audit or scanner service",
                purpose="White-label delivery, public intake, deployment routing, SSO starter planning, and billing starter planning.",
                best_for=[
                    "client-facing scanner",
                    "white-label audit delivery",
                    "self-hosted productization",
                ],
                first_class_paths=[
                    "ONE_DAY_SERVICE_BLUEPRINT.md",
                    "/api/v1/settings/service-foundation",
                    "/api/v1/settings/product-modes",
                ],
                not_the_goal=[
                    "maintainer-operated hosted SaaS",
                    "instant enterprise SLA out of the box",
                ],
            ),
        ]
    )


@router.get("/service-foundation", response_model=ServiceFoundationRead)
def service_foundation() -> ServiceFoundationRead:
    return ServiceFoundationRead(
        positioning=(
            "Use this repository as a self-hosted product foundation for a branded "
            "scanner, audit service, or operator platform."
        ),
        production_surfaces=[
            "scanner intake page",
            "workspace and project model",
            "provider and integration layer",
            "executive dashboard",
            "notifications and export artifacts",
            "governed CMS change flow",
        ],
        onboarding_layers=[
            "15-minute local or VPS bootstrap",
            "AI-agent-first deployment entrypoints",
            "white-label operator console",
            "public scan intake with queue boundaries",
            "SEO intelligence and RU/Yandex operating loops",
        ],
        sso_starter_modes=[
            "reverse-proxy auth header mode",
            "OIDC gateway with Authentik or Keycloak",
            "hosted IdP integration planning for Auth0 or Clerk",
        ],
        billing_starter_modes=[
            "free self-hosted internal mode",
            "manual invoice or contract mode",
            "Stripe checkout-links or sales-assisted mode",
            "workspace-plan gating as an operator policy layer",
        ],
        public_service_controls=[
            "rate limits and queue ceilings",
            "ownership verification for active scans",
            "notification hooks and operator review",
            "managed API boundary and product-mode separation",
        ],
        deployment_targets=[
            "Docker on VPS",
            "Coolify",
            "Railway",
            "Render",
            "Kubernetes starter pack",
        ],
        not_yet_turnkey=[
            "enterprise SLA",
            "fully managed hosted service run by maintainers",
            "complete live billing automation out of the box",
            "complete enterprise SSO implementation out of the box",
        ],
        best_next_steps=[
            "choose your deployment target",
            "choose one SSO strategy or stay with native auth first",
            "choose one billing strategy or stay free and internal first",
            "connect Google search, analytics, and paid stack",
            "connect Yandex search, analytics, and paid stack",
            "connect keyword, competitor, authority, and rank intelligence sources",
            "add local-business and distribution layers only after core search truth is in place",
            "enable integrations and scanner intake under your own domain",
        ],
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


def _integration_metrics_by_source(
    integrations: list[IntegrationConnection],
) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    for row in integrations:
        snapshot = json.loads(row.latest_snapshot_json or "{}")
        rows[row.source_type] = {
            "label": row.label,
            "status": row.last_sync_status or "created",
            "metrics": snapshot.get("metrics") or {},
            "rows": snapshot.get("rows") or [],
            "campaigns": snapshot.get("campaigns") or [],
            "locations": snapshot.get("locations") or [],
            "profiles": snapshot.get("profiles") or [],
            "videos": snapshot.get("videos") or [],
            "channels": snapshot.get("channels") or [],
            "top_pages": snapshot.get("top_pages") or [],
            "competitors": snapshot.get("competitors") or [],
            "opportunities": snapshot.get("opportunities") or [],
        }
    return rows


def _first_numeric(mapping: dict[str, object], key: str, default: float = 0.0) -> float:
    value = mapping.get(key, default)
    if isinstance(value, (int, float)):
        return float(value)
    return default


def _parse_ai_citation_score(mention_summary: str) -> float:
    marker = "AI Citation Score:"
    if marker not in mention_summary:
        return 0.0
    try:
        tail = mention_summary.split(marker, 1)[1].strip().split()[0]
        return float(tail)
    except (ValueError, IndexError):
        return 0.0


@router.get("/seo-intelligence-center")
def seo_intelligence_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    integrations = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    integration_metrics = _integration_metrics_by_source(integrations)
    keyword_metrics = (
        integration_metrics.get("keyword_research", {}).get("metrics") or {}
    )
    competitor_metrics = (
        integration_metrics.get("competitor_intelligence", {}).get("metrics") or {}
    )
    backlink_metrics = (
        integration_metrics.get("backlink_intelligence", {}).get("metrics") or {}
    )
    rank_metrics = integration_metrics.get("rank_tracking", {}).get("metrics") or {}

    connected_surfaces = [
        source
        for source in [
            "keyword_research",
            "competitor_intelligence",
            "backlink_intelligence",
            "rank_tracking",
        ]
        if source in integration_metrics
    ]
    opportunities = []
    for source in connected_surfaces:
        opportunities.extend(integration_metrics[source].get("opportunities") or [])

    return {
        "project_id": project_id,
        "connected_surfaces": connected_surfaces,
        "surface_contracts": [
            integration_contract(source) for source in connected_surfaces
        ],
        "scorecard": {
            "tracked_keywords": _first_numeric(keyword_metrics, "tracked_keywords"),
            "query_cluster_coverage": _first_numeric(
                keyword_metrics, "query_cluster_coverage"
            ),
            "tracked_competitors": _first_numeric(
                competitor_metrics, "tracked_competitors"
            ),
            "content_gap_count": _first_numeric(
                competitor_metrics, "content_gap_count"
            ),
            "referring_domains": _first_numeric(backlink_metrics, "referring_domains"),
            "authority_trend": _first_numeric(backlink_metrics, "authority_trend"),
            "top_10_share": _first_numeric(rank_metrics, "top_10_share"),
            "visibility_delta_30d": _first_numeric(
                rank_metrics, "visibility_delta_30d"
            ),
        },
        "operator_loops": [
            "map keyword demand to landing and content coverage",
            "compare competitors by content, proof, and GEO gaps",
            "separate authority recovery from content production work",
            "treat positions 4-12 as the first rank-ops lane",
        ],
        "practical_toolkit": [
            "scripts/checklist_generator.py",
            "scripts/semantic_gap_mapper.py",
            "scripts/serp-intent-cluster-helper.py",
            "scripts/content-inventory-helper.py",
        ],
        "provider_strategy": {
            "native_repo_mode": "starter stubs, exports, and provider-agnostic contracts",
            "external_provider_mode": "connect any approved keyword, competitor, backlink, or rank provider through the same contract surface",
            "ai_agent_mode": "give an AI coding agent the repo plus these surfaces to generate briefs, priorities, and change packs",
        },
        "opportunities": opportunities[:8],
    }


def _project_rollup(db: Session, project: Project) -> dict[str, object]:
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project.id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    latest_sov = (
        db.query(SovRun)
        .filter(SovRun.project_id == project.id)
        .order_by(SovRun.id.desc())
        .first()
    )
    reports_count = db.query(Report).filter(Report.project_id == project.id).count()
    evidence_count = (
        db.query(EvidenceRecord).filter(EvidenceRecord.project_id == project.id).count()
    )
    experiment_count = (
        db.query(ExperimentRecord)
        .filter(ExperimentRecord.project_id == project.id)
        .count()
    )
    return {
        "project_id": project.id,
        "project_name": project.name,
        "website_url": project.website_url,
        "latest_audit_score": latest_audit.summary_score if latest_audit else None,
        "latest_audit_status": latest_audit.status if latest_audit else "not_run",
        "latest_ai_citation_score": _parse_ai_citation_score(latest_sov.mention_summary)
        if latest_sov
        else 0.0,
        "share_estimate": latest_sov.share_estimate if latest_sov else None,
        "reports_count": reports_count,
        "evidence_count": evidence_count,
        "experiment_count": experiment_count,
    }


@router.get("/portfolio-dashboard")
def portfolio_dashboard(
    workspace_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    accessible_workspace_ids = {
        row.id
        for row in db.query(Workspace)
        .filter(Workspace.owner_user_id == current_user.id)
        .all()
    }
    accessible_workspace_ids.update(
        row.workspace_id
        for row in db.query(WorkspaceMembership)
        .filter(WorkspaceMembership.user_id == current_user.id)
        .all()
    )
    if workspace_id is not None:
        require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
        workspace_ids = [workspace_id]
    elif organization_id is not None:
        workspace_ids = [
            row.workspace_id
            for row in db.query(TenantProfile)
            .filter(TenantProfile.organization_id == organization_id)
            .all()
            if row.workspace_id in accessible_workspace_ids
        ]
    else:
        workspace_ids = sorted(accessible_workspace_ids)
    projects = (
        db.query(Project)
        .filter(Project.workspace_id.in_(workspace_ids or [0]))
        .order_by(Project.id.asc())
        .all()
    )
    rows = [_project_rollup(db, project) for project in projects]
    audit_scores = [
        row["latest_audit_score"]
        for row in rows
        if row["latest_audit_score"] is not None
    ]
    citation_scores = [
        row["latest_ai_citation_score"]
        for row in rows
        if row["latest_ai_citation_score"]
    ]
    workspace_breakdown = []
    for target_workspace_id in workspace_ids:
        workspace_rows = [
            row
            for row, project in zip(rows, projects)
            if project.workspace_id == target_workspace_id
        ]
        workspace = db.get(Workspace, target_workspace_id)
        workspace_breakdown.append(
            {
                "workspace_id": target_workspace_id,
                "workspace_name": workspace.name
                if workspace
                else f"Workspace {target_workspace_id}",
                "project_count": len(workspace_rows),
                "average_audit_score": round(
                    sum(
                        item["latest_audit_score"]
                        for item in workspace_rows
                        if item["latest_audit_score"] is not None
                    )
                    / max(
                        1,
                        len(
                            [
                                item
                                for item in workspace_rows
                                if item["latest_audit_score"] is not None
                            ]
                        ),
                    ),
                    1,
                )
                if any(
                    item["latest_audit_score"] is not None for item in workspace_rows
                )
                else None,
            }
        )
    return {
        "workspace_id": workspace_id,
        "organization_id": organization_id,
        "workspace_ids": workspace_ids,
        "project_count": len(rows),
        "portfolio_summary": {
            "average_audit_score": round(sum(audit_scores) / len(audit_scores), 1)
            if audit_scores
            else None,
            "average_ai_citation_score": round(
                sum(citation_scores) / len(citation_scores), 1
            )
            if citation_scores
            else None,
            "projects_with_proof": sum(1 for row in rows if row["evidence_count"]),
            "projects_with_experiments": sum(
                1 for row in rows if row["experiment_count"]
            ),
            "projects_needing_attention": sum(
                1
                for row in rows
                if row["latest_audit_score"] is not None
                and row["latest_audit_score"] < 70
            ),
        },
        "workspace_breakdown": workspace_breakdown,
        "projects": rows,
    }


@router.get("/mention-reputation-center")
def mention_reputation_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    sov_runs = (
        db.query(SovRun)
        .filter(SovRun.project_id == project_id)
        .order_by(SovRun.id.desc())
        .limit(10)
        .all()
    )
    evidence_rows = (
        db.query(EvidenceRecord)
        .filter(EvidenceRecord.project_id == project_id)
        .order_by(EvidenceRecord.id.desc())
        .limit(10)
        .all()
    )
    ai_scores = [
        _parse_ai_citation_score(row.mention_summary)
        for row in sov_runs
        if row.mention_summary
    ]
    return {
        "project_id": project.id,
        "project_name": project.name,
        "overview": {
            "latest_ai_citation_score": ai_scores[0] if ai_scores else 0.0,
            "average_recent_ai_citation_score": round(
                sum(ai_scores) / len(ai_scores), 1
            )
            if ai_scores
            else 0.0,
            "evidence_records": len(evidence_rows),
            "tracking_mode": "operator-proof + AI SoV history",
        },
        "tracking_layers": [
            "AI mention and citation history",
            "proof-linked reputation events",
            "local-business trust overlays",
            "social/distribution connectors",
            "RU community and Yandex trust overlays",
        ],
        "commercial_use_cases": [
            "show how community demand supports search demand",
            "prove trust growth with local-business and review signals",
            "tie AI visibility to social proof and repeated objections",
        ],
        "latest_mentions": [
            {
                "id": row.id,
                "brand": row.brand,
                "share_estimate": row.share_estimate,
                "mention_summary": row.mention_summary,
                "created_at": row.created_at.isoformat(),
            }
            for row in sov_runs[:5]
        ],
        "reputation_events": [
            {
                "id": row.id,
                "label_type": row.label_type,
                "title": row.title,
                "summary": row.summary,
                "created_at": row.created_at.isoformat(),
            }
            for row in evidence_rows[:5]
        ],
    }


@router.get("/operator-board")
def operator_board(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project_id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    if not latest_audit:
        return {
            "project_id": project_id,
            "tasks": [],
            "board_columns": ["open", "in_review", "verify", "rollback_ready"],
            "summary": {"total_tasks": 0, "verify_ready": 0, "rollback_ready": 0},
        }
    findings = json.loads(latest_audit.finding_groups_json or "[]")
    bundle = build_task_bundle_from_audit_run(latest_audit, findings)
    tasks = []
    for index, task in enumerate(bundle["tasks"], start=1):
        tasks.append(
            {
                "task_id": task["id"],
                "title": task["recommended_fix"],
                "owner": task["suggested_owner"],
                "status": "verify" if task["severity"] == "high" else "open",
                "verify_step": "rerun audit and compare proof timeline",
                "rollback_step": "revert CMS or code patch if regression appears",
                "priority": task["severity"],
                "source_ref": task["source_ref"],
                "sort_order": index,
            }
        )
    return {
        "project_id": project_id,
        "generated_from_audit_run": latest_audit.id,
        "board_columns": ["open", "in_review", "verify", "rollback_ready"],
        "summary": {
            "total_tasks": len(tasks),
            "verify_ready": len([task for task in tasks if task["status"] == "verify"]),
            "rollback_ready": len(
                [task for task in tasks if task["status"] == "rollback_ready"]
            ),
        },
        "lane_counts": {
            lane: len([task for task in tasks if task["status"] == lane])
            for lane in ["open", "in_review", "verify", "rollback_ready"]
        },
        "tasks": tasks,
    }


@router.get("/proof-ops-center")
def proof_ops_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    evidence_rows = (
        db.query(EvidenceRecord)
        .filter(EvidenceRecord.project_id == project_id)
        .order_by(EvidenceRecord.id.desc())
        .all()
    )
    experiment_rows = (
        db.query(ExperimentRecord)
        .filter(ExperimentRecord.project_id == project_id)
        .order_by(ExperimentRecord.id.desc())
        .all()
    )
    confidence_counts = {"weak": 0, "partial": 0, "strong": 0}
    for row in experiment_rows:
        confidence_counts[row.confidence_label] = (
            confidence_counts.get(row.confidence_label, 0) + 1
        )
    return {
        "project_id": project.id,
        "project_name": project.name,
        "summary": {
            "evidence_count": len(evidence_rows),
            "experiment_count": len(experiment_rows),
            "strong_experiments": confidence_counts.get("strong", 0),
            "public_fact_records": len(
                [row for row in evidence_rows if row.label_type == "public_fact"]
            ),
        },
        "confidence_distribution": confidence_counts,
        "recent_evidence": [
            {
                "id": row.id,
                "title": row.title,
                "label_type": row.label_type,
                "summary": row.summary,
                "created_at": row.created_at.isoformat(),
            }
            for row in evidence_rows[:5]
        ],
        "recent_experiments": [
            {
                "id": row.id,
                "source_type": row.source_type,
                "source_id": row.source_id,
                "confidence_label": row.confidence_label,
                "change_summary": row.change_summary,
                "created_at": row.created_at.isoformat(),
            }
            for row in experiment_rows[:5]
        ],
        "recommended_next_steps": [
            "capture at least one public before/after proof item per major fix lane",
            "promote strong experiments into client-safe exports and case libraries",
            "attach evidence links to rollback or verify steps in the operator board",
        ],
    }


@router.get("/runtime-ops-center")
def runtime_ops_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    cms_rows = (
        db.query(CmsConnector)
        .filter(CmsConnector.project_id == project_id)
        .order_by(CmsConnector.id.desc())
        .all()
    )
    latest_events = {}
    if integration_rows:
        event_rows = (
            db.query(IntegrationSyncEvent)
            .filter(
                IntegrationSyncEvent.integration_connection_id.in_(
                    [row.id for row in integration_rows]
                )
            )
            .order_by(IntegrationSyncEvent.id.desc())
            .all()
        )
        for row in event_rows:
            latest_events.setdefault(row.integration_connection_id, row)

    matrix = []
    token_rotation_queue = []
    refresh_queue = []
    recovery_queue = []
    for row in integration_rows:
        latest_snapshot = json.loads(row.latest_snapshot_json or "{}")
        runtime_profile = integration_runtime_profile(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=latest_snapshot,
        )
        diagnostics = integration_runtime_profile(
            row.source_type,
            config=json.loads(row.config_json or "{}"),
            credentials_env_var=row.credentials_env_var,
            latest_snapshot=latest_snapshot,
        )
        latest_event = latest_events.get(row.id)
        last_status = (
            latest_event.status if latest_event else row.last_sync_status or "created"
        )
        refresh_minutes = runtime_profile["refresh_minutes"]
        rotation_days = runtime_profile["token_rotation_days"]
        retry_backoff = runtime_profile["retry_backoff_minutes"]
        needs_rotation = rotation_days <= 30
        needs_refresh = refresh_minutes > 1440
        needs_recovery = (
            last_status == "failed"
            or runtime_profile["failure_recovery_mode"] != "retry_then_operator_review"
        )
        matrix.append(
            {
                "integration_id": row.id,
                "label": row.label,
                "source_type": row.source_type,
                "runtime_level": runtime_profile["runtime_level"],
                "managed_runtime_enabled": runtime_profile["managed_runtime_enabled"],
                "refresh_minutes": refresh_minutes,
                "token_rotation_days": rotation_days,
                "retry_backoff_minutes": retry_backoff,
                "failure_recovery_mode": runtime_profile["failure_recovery_mode"],
                "last_status": last_status,
                "next_operator_action": (
                    "rotate_token"
                    if needs_rotation
                    else "tighten_refresh_cadence"
                    if needs_refresh
                    else "review_failure_recovery"
                    if needs_recovery
                    else "monitor"
                ),
                "status": (
                    "attention"
                    if needs_rotation or needs_refresh or needs_recovery
                    else "healthy"
                ),
                "diagnostics": diagnostics,
            }
        )
        if needs_rotation:
            token_rotation_queue.append(
                {
                    "integration_id": row.id,
                    "label": row.label,
                    "source_type": row.source_type,
                    "token_rotation_days": rotation_days,
                    "reason": "rotation window is too short or about to expire",
                }
            )
        if needs_refresh:
            refresh_queue.append(
                {
                    "integration_id": row.id,
                    "label": row.label,
                    "refresh_minutes": refresh_minutes,
                    "recommended_target": 1440,
                }
            )
        if needs_recovery:
            recovery_queue.append(
                {
                    "integration_id": row.id,
                    "label": row.label,
                    "last_status": last_status,
                    "failure_recovery_mode": runtime_profile["failure_recovery_mode"],
                    "retry_backoff_minutes": retry_backoff,
                }
            )

    cms_writeback_queue = [
        {
            "cms_connector_id": row.id,
            "label": row.label,
            "cms_type": row.cms_type,
            "writeback_mode": row.writeback_mode,
            "action": (
                "verify_preview_and_rollback"
                if row.writeback_mode != "read_only"
                else "keep_read_only_until_operator_approval"
            ),
        }
        for row in cms_rows
    ]
    return {
        "project_id": project.id,
        "project_name": project.name,
        "summary": {
            "integration_count": len(integration_rows),
            "cms_count": len(cms_rows),
            "managed_runtime_count": len(
                [row for row in matrix if row["runtime_level"] == "managed_runtime"]
            ),
            "attention_count": len(
                [row for row in matrix if row["status"] == "attention"]
            ),
            "token_rotations_due": len(token_rotation_queue),
            "refresh_actions_due": len(refresh_queue),
            "recovery_actions_due": len(recovery_queue),
        },
        "managed_runtime_matrix": matrix,
        "token_rotation_queue": token_rotation_queue,
        "refresh_queue": refresh_queue,
        "recovery_queue": recovery_queue,
        "cms_writeback_queue": cms_writeback_queue,
        "operator_runbook": [
            "keep high-signal demand sources at daily or better refresh cadence",
            "treat token rotation as an operator calendar, not an afterthought",
            "use retries for transient failures and explicit review for structural failures",
            "pair CMS apply flows with preview, verify, and rollback steps",
        ],
    }


@router.get("/seo-maturity-center")
def seo_maturity_center(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    integration_rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project_id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    integration_metrics = _integration_metrics_by_source(integration_rows)
    keyword_metrics = (
        integration_metrics.get("keyword_research", {}).get("metrics") or {}
    )
    competitor_metrics = (
        integration_metrics.get("competitor_intelligence", {}).get("metrics") or {}
    )
    backlink_metrics = (
        integration_metrics.get("backlink_intelligence", {}).get("metrics") or {}
    )
    rank_metrics = integration_metrics.get("rank_tracking", {}).get("metrics") or {}
    gsc_rows = integration_metrics.get("gsc", {}).get("rows") or []
    findings = (
        json.loads(latest_audit.finding_groups_json or "[]") if latest_audit else []
    )

    semantic_score = min(
        1.0,
        (
            (_first_numeric(keyword_metrics, "query_cluster_coverage"))
            + (0.2 if len(gsc_rows) >= 5 else 0)
            + (0.2 if findings else 0)
        ),
    )
    competitor_score = min(
        1.0,
        (_first_numeric(competitor_metrics, "tracked_competitors") / 5)
        + _first_numeric(competitor_metrics, "content_gap_count") / 20,
    )
    authority_score = min(
        1.0,
        (_first_numeric(backlink_metrics, "referring_domains") / 100)
        + max(0.0, _first_numeric(backlink_metrics, "authority_trend")),
    )
    measurement_score = min(
        1.0,
        (_first_numeric(rank_metrics, "top_10_share"))
        + (0.25 if "gsc" in integration_metrics else 0)
        + (0.25 if "ga4" in integration_metrics else 0),
    )
    tracks = [
        {
            "track": "semantic_core",
            "status": _maturity_status(semantic_score),
            "score": round(semantic_score, 2),
            "evidence": {
                "query_cluster_coverage": _first_numeric(
                    keyword_metrics, "query_cluster_coverage"
                ),
                "gsc_query_rows": len(gsc_rows),
            },
            "next_steps": [
                "expand demand clusters into page and FAQ assets",
                "map intent gaps between core landing pages and informational support",
            ],
        },
        {
            "track": "competitor_workflows",
            "status": _maturity_status(competitor_score),
            "score": round(competitor_score, 2),
            "evidence": {
                "tracked_competitors": _first_numeric(
                    competitor_metrics, "tracked_competitors"
                ),
                "content_gap_count": _first_numeric(
                    competitor_metrics, "content_gap_count"
                ),
            },
            "next_steps": [
                "turn competitor gaps into owned content or proof lanes",
                "compare category, service, and FAQ coverage against live rivals",
            ],
        },
        {
            "track": "authority_and_links",
            "status": _maturity_status(authority_score),
            "score": round(authority_score, 2),
            "evidence": {
                "referring_domains": _first_numeric(
                    backlink_metrics, "referring_domains"
                ),
                "authority_trend": _first_numeric(backlink_metrics, "authority_trend"),
            },
            "next_steps": [
                "separate authority recovery from content production",
                "build linkable proof assets instead of generic outreach asks",
            ],
        },
        {
            "track": "measurement_and_benchmarks",
            "status": _maturity_status(measurement_score),
            "score": round(measurement_score, 2),
            "evidence": {
                "top_10_share": _first_numeric(rank_metrics, "top_10_share"),
                "has_gsc": "gsc" in integration_metrics,
                "has_ga4": "ga4" in integration_metrics,
            },
            "next_steps": [
                "pair rank tracking with GSC and analytics, not rankings alone",
                "review benchmark deltas before and after every major fix cycle",
            ],
        },
    ]
    return {
        "project_id": project.id,
        "project_name": project.name,
        "summary": {
            "overall_status": _maturity_status(
                sum(item["score"] for item in tracks) / len(tracks)
            ),
            "tracks": len(tracks),
            "latest_audit_id": latest_audit.id if latest_audit else None,
            "finding_count": len(findings),
        },
        "tracks": tracks,
        "benchmark_datasets": [
            "query cluster coverage",
            "competitor gap count",
            "referring domains and authority trend",
            "tracked-query top-10 share",
            "GSC plus GA4 outcome loop",
        ],
        "operator_rule": (
            "Do not treat GEO or AI visibility as a replacement for semantic, "
            "competitor, authority, and measurement depth."
        ),
    }


@router.get("/evidence-lab")
def evidence_lab(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    evidence_rows = (
        db.query(EvidenceRecord)
        .filter(EvidenceRecord.project_id == project_id)
        .order_by(EvidenceRecord.id.desc())
        .all()
    )
    experiment_rows = (
        db.query(ExperimentRecord)
        .filter(ExperimentRecord.project_id == project_id)
        .order_by(ExperimentRecord.id.desc())
        .all()
    )
    reports = (
        db.query(Report)
        .filter(Report.project_id == project_id)
        .order_by(Report.id.desc())
        .all()
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project_id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    strong_experiments = [
        row for row in experiment_rows if row.confidence_label == "strong"
    ]
    return {
        "project_id": project.id,
        "project_name": project.name,
        "summary": {
            "evidence_records": len(evidence_rows),
            "experiments": len(experiment_rows),
            "strong_experiments": len(strong_experiments),
            "reports": len(reports),
            "latest_audit_id": latest_audit.id if latest_audit else None,
        },
        "publishable_assets": [
            {
                "asset": "before_after_case_note",
                "ready": bool(evidence_rows and experiment_rows),
            },
            {
                "asset": "client_safe_export_pack",
                "ready": bool(reports),
            },
            {
                "asset": "operator_proof_timeline",
                "ready": bool(experiment_rows),
            },
            {
                "asset": "synthetic_training_case",
                "ready": True,
            },
            {
                "asset": "issue_pack",
                "ready": bool(latest_audit or experiment_rows),
            },
        ],
        "case_library_targets": [
            {
                "id": "anmalishev_ru",
                "paths": [
                    "REAL_CASES.md",
                    "REAL_CASES_RU.md",
                    "docs/en/v430-case-anmalishev.md",
                    "docs/ru/v430-case-anmalishev.md",
                ],
            },
            {
                "id": "auditguard_ru",
                "paths": ["REAL_CASES.md", "REAL_CASES_RU.md"],
            },
            {
                "id": "sitepravo_ru",
                "paths": ["REAL_CASES.md", "REAL_CASES_RU.md"],
            },
            {
                "id": "case_library",
                "paths": [
                    "docs/en/case-library.md",
                    "docs/ru/case-library.md",
                ],
            },
        ],
        "independent_proof_targets": [
            "attach GSC, GA4, or Yandex screenshots to major before/after claims",
            "promote strong experiments into reusable public case formats",
            "export at least one client-safe markdown pack per high-impact fix cycle",
        ],
        "tooling": [
            "scripts/proof_pack_builder.py",
            "scripts/case_library_builder.py",
            "scripts/synthetic_case_builder.py",
            "scripts/issue_pack_generator.py",
        ],
        "recent_assets": [
            {
                "kind": "evidence",
                "title": row.title,
                "summary": row.summary,
            }
            for row in evidence_rows[:3]
        ]
        + [
            {
                "kind": "experiment",
                "title": row.change_summary,
                "summary": row.confidence_label,
            }
            for row in experiment_rows[:3]
        ],
    }


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
    integration_metrics = _integration_metrics_by_source(integrations)
    gsc_metrics = integration_metrics.get("gsc", {}).get("rows") or []
    ga4_metrics = integration_metrics.get("ga4", {}).get("metrics") or {}
    google_ads_metrics = integration_metrics.get("google_ads", {}).get("metrics") or {}
    webmaster_metrics = (
        integration_metrics.get("yandex_webmaster", {}).get("rows") or []
    )
    metrica_metrics = integration_metrics.get("yandex_metrica", {}).get("metrics") or {}
    direct_metrics = integration_metrics.get("yandex_direct", {}).get("metrics") or {}
    keyword_metrics = (
        integration_metrics.get("keyword_research", {}).get("metrics") or {}
    )
    competitor_metrics = (
        integration_metrics.get("competitor_intelligence", {}).get("metrics") or {}
    )
    backlink_metrics = (
        integration_metrics.get("backlink_intelligence", {}).get("metrics") or {}
    )
    rank_metrics = integration_metrics.get("rank_tracking", {}).get("metrics") or {}
    crux_metrics = integration_metrics.get("crux", {}).get("metrics") or {}
    gbp_metrics = (
        integration_metrics.get("google_business_profile", {}).get("metrics") or {}
    )
    yb_metrics = integration_metrics.get("yandex_business", {}).get("metrics") or {}
    merchant_metrics = (
        integration_metrics.get("merchant_center", {}).get("metrics") or {}
    )
    alice_metrics = (
        integration_metrics.get("alice_ai_visibility", {}).get("metrics") or {}
    )
    alice_rows = integration_metrics.get("alice_ai_visibility", {}).get("rows") or []
    alice_competitors = (
        integration_metrics.get("alice_ai_visibility", {}).get("competitors") or []
    )
    meta_metrics = integration_metrics.get("meta_ads", {}).get("metrics") or {}
    x_ads_metrics = integration_metrics.get("x_ads", {}).get("metrics") or {}
    x_organic_metrics = integration_metrics.get("x_organic", {}).get("metrics") or {}
    threads_metrics = integration_metrics.get("threads", {}).get("metrics") or {}
    reddit_metrics = integration_metrics.get("reddit_mentions", {}).get("metrics") or {}
    tiktok_metrics = integration_metrics.get("tiktok_organic", {}).get("metrics") or {}
    vk_metrics = integration_metrics.get("vk_ads", {}).get("metrics") or {}
    telegram_metrics = integration_metrics.get("telegram_ads", {}).get("metrics") or {}
    youtube_metrics = integration_metrics.get("youtube", {}).get("metrics") or {}
    linkedin_metrics = integration_metrics.get("linkedin_ads", {}).get("metrics") or {}
    instagram_metrics = (
        integration_metrics.get("instagram_facebook_organic", {}).get("metrics") or {}
    )
    ru_geo_score_value, ru_geo_components = ru_geo_score(
        integration_metrics=integration_metrics
    )
    alice_ai_sov = _first_numeric(alice_metrics, "share_of_voice")
    alice_ai_weekly_delta = _first_numeric(alice_metrics, "weekly_delta")
    alice_ai_query_coverage = _first_numeric(alice_metrics, "query_coverage")
    alice_ai_status = benchmark_status("alice_ai_sov", alice_ai_sov)
    executive_layers = {
        "google_executive_layer": {
            "sources": ["gsc", "ga4", "google_ads", "crux"],
            "connected": [
                source
                for source in ["gsc", "ga4", "google_ads", "crux"]
                if source in integration_metrics
            ],
            "focus": "organic demand, paid demand, user behavior, and field data",
        },
        "seo_intelligence_layer": {
            "sources": [
                "keyword_research",
                "competitor_intelligence",
                "backlink_intelligence",
                "rank_tracking",
            ],
            "connected": [
                source
                for source in [
                    "keyword_research",
                    "competitor_intelligence",
                    "backlink_intelligence",
                    "rank_tracking",
                ]
                if source in integration_metrics
            ],
            "focus": "market demand, competitor gaps, authority, and tracked visibility",
        },
        "ru_executive_layer": {
            "sources": [
                "yandex_webmaster",
                "yandex_metrica",
                "yandex_direct",
                "alice_ai_visibility",
            ],
            "connected": [
                source
                for source in [
                    "yandex_webmaster",
                    "yandex_metrica",
                    "yandex_direct",
                    "alice_ai_visibility",
                ]
                if source in integration_metrics
            ],
            "focus": "RU visibility, RU analytics, Alice AI visibility, and RU paid demand",
        },
        "local_business_layer": {
            "sources": [
                "google_business_profile",
                "yandex_business",
                "merchant_center",
            ],
            "connected": [
                source
                for source in [
                    "google_business_profile",
                    "yandex_business",
                    "merchant_center",
                ]
                if source in integration_metrics
            ],
            "focus": "maps trust, local demand, and e-commerce feed health",
        },
        "distribution_layer": {
            "sources": [
                "meta_ads",
                "x_ads",
                "x_organic",
                "threads",
                "reddit_mentions",
                "tiktok_organic",
                "vk_ads",
                "telegram_ads",
                "youtube",
                "linkedin_ads",
                "instagram_facebook_organic",
            ],
            "connected": [
                source
                for source in [
                    "meta_ads",
                    "x_ads",
                    "x_organic",
                    "threads",
                    "reddit_mentions",
                    "tiktok_organic",
                    "vk_ads",
                    "telegram_ads",
                    "youtube",
                    "linkedin_ads",
                    "instagram_facebook_organic",
                ]
                if source in integration_metrics
            ],
            "focus": "distribution, audience demand, and supporting paid or social context",
        },
        "ru_geo_ai_layer": {
            "connected": [
                source
                for source in [
                    "yandex_neuro",
                    "alice_ai_visibility",
                    "yandex_business",
                ]
                if source in integration_metrics
            ],
            "focus": "YandexAdditional access, Alice AI SoV, and RU answer-ready trust signals",
            "signals": [
                "YandexBot",
                "YandexAdditional",
                "Alice AI share of voice",
                "RU entity readiness",
                "RU answer-ready content",
                "RU snippets and trust blocks",
            ],
        },
    }
    comparison_metrics = {
        "organic_demand": {
            "google_clicks": sum(
                int(item.get("clicks", 0)) for item in gsc_metrics[:10]
            ),
            "yandex_clicks": sum(
                int(item.get("clicks", 0)) for item in webmaster_metrics[:10]
            ),
        },
        "paid_demand": {
            "google_ads_cost": _first_numeric(google_ads_metrics, "cost"),
            "google_ads_conversions": _first_numeric(google_ads_metrics, "conversions"),
            "yandex_direct_cost": _first_numeric(direct_metrics, "spend"),
            "yandex_direct_conversions": _first_numeric(direct_metrics, "conversions"),
        },
        "ai_visibility": {
            "share_of_citation": round(executive_score / 100, 3),
            "share_of_demand_brand": max(
                _first_numeric(google_ads_metrics, "brand_share_of_demand"),
                _first_numeric(direct_metrics, "brand_share_of_demand"),
            ),
            "alice_ai_share_of_voice": alice_ai_sov,
            "alice_ai_weekly_delta": alice_ai_weekly_delta,
            "alice_ai_query_coverage": alice_ai_query_coverage,
            "alice_ai_status": alice_ai_status,
            "alice_ai_insufficient_data": bool(alice_metrics.get("insufficient_data")),
        },
        "landing_page_conversion": {
            "ga4_engagement_rate": _first_numeric(ga4_metrics, "engagement_rate"),
            "ga4_sessions": _first_numeric(ga4_metrics, "sessions"),
            "metrica_goal_completion_rate": _first_numeric(
                metrica_metrics, "goal_completion_rate"
            ),
            "metrica_visits": _first_numeric(metrica_metrics, "visits"),
        },
        "efficiency": {
            "ctr_google_ads": _first_numeric(google_ads_metrics, "ctr"),
            "ctr_yandex_direct": _first_numeric(direct_metrics, "ctr"),
            "cpa_google_ads": _first_numeric(google_ads_metrics, "cpa"),
            "cpa_yandex_direct": _first_numeric(direct_metrics, "cost_per_conversion"),
            "cpl_meta_ads": _first_numeric(meta_metrics, "cpl"),
            "cpl_x_ads": _first_numeric(x_ads_metrics, "cpl"),
            "cpl_vk_ads": _first_numeric(vk_metrics, "cpl"),
            "cpl_linkedin_ads": _first_numeric(linkedin_metrics, "cpl"),
        },
        "local_and_commerce": {
            "google_business_reviews": _first_numeric(gbp_metrics, "review_count"),
            "yandex_business_reviews": _first_numeric(yb_metrics, "review_count"),
            "merchant_approval_rate": _first_numeric(merchant_metrics, "approval_rate"),
        },
        "distribution": {
            "x_organic_site_clicks": _first_numeric(x_organic_metrics, "site_clicks"),
            "threads_site_clicks": _first_numeric(threads_metrics, "site_clicks"),
            "reddit_site_clicks": _first_numeric(reddit_metrics, "site_clicks"),
            "tiktok_site_clicks": _first_numeric(tiktok_metrics, "site_clicks"),
            "telegram_clicks": _first_numeric(telegram_metrics, "clicks"),
            "youtube_site_clicks": _first_numeric(youtube_metrics, "site_clicks"),
            "instagram_site_clicks": _first_numeric(instagram_metrics, "site_clicks"),
        },
        "seo_intelligence": {
            "tracked_keywords": _first_numeric(keyword_metrics, "tracked_keywords"),
            "query_cluster_coverage": _first_numeric(
                keyword_metrics, "query_cluster_coverage"
            ),
            "tracked_competitors": _first_numeric(
                competitor_metrics, "tracked_competitors"
            ),
            "content_gap_count": _first_numeric(
                competitor_metrics, "content_gap_count"
            ),
            "referring_domains": _first_numeric(backlink_metrics, "referring_domains"),
            "authority_trend": _first_numeric(backlink_metrics, "authority_trend"),
            "top_10_share": _first_numeric(rank_metrics, "top_10_share"),
            "visibility_delta_30d": _first_numeric(
                rank_metrics, "visibility_delta_30d"
            ),
        },
    }
    benchmark_overlays = {
        "seo_vs_geo_vs_paid": {
            "seo_strength": comparison_metrics["organic_demand"]["google_clicks"]
            + comparison_metrics["organic_demand"]["yandex_clicks"],
            "geo_strength": comparison_metrics["ai_visibility"]["share_of_citation"],
            "paid_strength": comparison_metrics["paid_demand"]["google_ads_cost"]
            + comparison_metrics["paid_demand"]["yandex_direct_cost"],
        },
        "local_trust_vs_lead_generation": {
            "review_count_total": _first_numeric(gbp_metrics, "review_count")
            + _first_numeric(yb_metrics, "review_count"),
            "conversion_signals": _first_numeric(ga4_metrics, "engagement_rate")
            + _first_numeric(metrica_metrics, "goal_completion_rate"),
        },
        "ru_stack_vs_google_stack": {
            "google_connected": len(
                executive_layers["google_executive_layer"]["connected"]
            ),
            "ru_connected": len(executive_layers["ru_executive_layer"]["connected"]),
        },
        "ru_ai_answer_visibility": {
            "alice_ai_sov": alice_ai_sov,
            "alice_ai_weekly_delta": alice_ai_weekly_delta,
            "ru_geo_score": ru_geo_score_value,
            "tracked_competitors": len(alice_competitors),
        },
        "seo_intelligence_posture": {
            "tracked_keywords": _first_numeric(keyword_metrics, "tracked_keywords"),
            "tracked_competitors": _first_numeric(
                competitor_metrics, "tracked_competitors"
            ),
            "authority_trend": _first_numeric(backlink_metrics, "authority_trend"),
            "top_10_share": _first_numeric(rank_metrics, "top_10_share"),
        },
    }
    anomalies: list[dict[str, object]] = []
    if _first_numeric(crux_metrics.get("largest_contentful_paint", {}), "p75") > 2500:
        anomalies.append(
            {
                "severity": "high",
                "surface": "crux",
                "message": "Field LCP is above the preferred threshold.",
                "likely_cause": "page weight or rendering bottlenecks",
            }
        )
    if (
        _first_numeric(google_ads_metrics, "cpa") > 20
        or _first_numeric(direct_metrics, "cost_per_conversion") > 20
    ):
        anomalies.append(
            {
                "severity": "medium",
                "surface": "paid_efficiency",
                "message": "Paid acquisition efficiency is softening.",
                "likely_cause": "keyword drift or landing-page mismatch",
            }
        )
    if bool(alice_metrics.get("insufficient_data")):
        anomalies.append(
            {
                "severity": "medium",
                "surface": "alice_ai_visibility",
                "message": "Alice AI visibility still has insufficient data for a stable weekly share-of-voice view.",
                "likely_cause": "the site has too few eligible Yandex impressions or too little citation presence",
            }
        )
    elif alice_ai_status == "urgent_fix":
        anomalies.append(
            {
                "severity": "high",
                "surface": "alice_ai_visibility",
                "message": "Alice AI share of voice is weak for the current RU search footprint.",
                "likely_cause": "answer-ready content, trust blocks, or cited source pages are not strong enough",
            }
        )
    if (
        "keyword_research" in integration_metrics
        and _first_numeric(keyword_metrics, "query_cluster_coverage") < 0.5
    ):
        anomalies.append(
            {
                "severity": "medium",
                "surface": "keyword_research",
                "message": "Query-cluster coverage is still thin for the tracked demand map.",
                "likely_cause": "too few dedicated landing or FAQ assets for major demand clusters",
            }
        )
    if (
        "rank_tracking" in integration_metrics
        and _first_numeric(rank_metrics, "top_10_share") < 0.4
    ):
        anomalies.append(
            {
                "severity": "medium",
                "surface": "rank_tracking",
                "message": "Tracked-query visibility is still weak across top-10 positions.",
                "likely_cause": "mid-SERP pages need stronger intent matching, proof density, or internal linking",
            }
        )
    owner_suggestions = [
        {
            "owner": "SEO strategist",
            "focus": "keyword demand, competitor gaps, authority recovery, and rank operations",
            "priority": "high",
        },
        {
            "owner": "SEO lead",
            "focus": "organic demand, indexation health, and answer-ready content",
            "priority": "high",
        },
        {
            "owner": "Growth or paid lead",
            "focus": "paid demand, CTR, CPA, and landing-page alignment",
            "priority": "medium",
        },
        {
            "owner": "Content or GEO lead",
            "focus": "AI visibility, brand-fact consistency, and citation share",
            "priority": "high",
        },
        {
            "owner": "RU market lead",
            "focus": "Alice AI visibility, YandexAdditional readiness, and Yandex commercial proof",
            "priority": "high",
        },
    ]
    operating_queue = [
        {
            "step": "refresh integrations",
            "owner": "operator",
            "status": "ready",
        },
        {
            "step": "review executive anomalies",
            "owner": "owner_or_admin",
            "status": "ready" if anomalies else "watch",
        },
        {
            "step": "capture proof delta",
            "owner": "analyst",
            "status": "ready",
        },
    ]
    portfolio_view = {
        "workspace_id": project.workspace_id,
        "project_name": project.name,
        "connected_surfaces_total": len(integrations) + len(cms_connectors),
        "seo_intelligence_surfaces": len(
            executive_layers["seo_intelligence_layer"]["connected"]
        ),
        "high_priority_items": len(
            [item for item in priorities if item["priority_score"] >= 70]
        ),
        "anomaly_count": len(anomalies),
        "ru_geo_score": ru_geo_score_value,
    }
    return ExecutiveDashboardRead(
        project_id=project.id,
        workspace_id=project.workspace_id,
        executive_score=executive_score,
        health_band=health_band,
        narrative=(
            f"{project.name} is in {health_band} condition. "
            "Use scanner intake, structured audits, integrations, CMS review gates, and CI-backed re-measurement as one operating loop."
        ),
        weekly_narrative=(
            f"This week {project.name} should focus on {len(priorities)} priority lanes, "
            f"{len(anomalies)} anomaly checks, {len(integrations)} connected integrations, "
            f"and Alice AI SoV at {alice_ai_sov:.2f}."
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
            "google_surface_connected": len(
                executive_layers["google_executive_layer"]["connected"]
            ),
            "seo_surface_connected": len(
                executive_layers["seo_intelligence_layer"]["connected"]
            ),
            "ru_surface_connected": len(
                executive_layers["ru_executive_layer"]["connected"]
            ),
            "distribution_surface_connected": len(
                executive_layers["distribution_layer"]["connected"]
            ),
            "local_surface_connected": len(
                executive_layers["local_business_layer"]["connected"]
            ),
            "alice_ai_surface_connected": int(
                "alice_ai_visibility" in integration_metrics
            ),
            "ru_geo_score": ru_geo_score_value,
            "ru_geo_status": benchmark_status("ru_geo_score", ru_geo_score_value),
            "alice_ai_sov": alice_ai_sov,
            "alice_ai_query_examples": len(alice_rows),
            "alice_ai_competitors_tracked": len(alice_competitors),
            "ru_geo_components": ru_geo_components,
            "tracked_keywords": _first_numeric(keyword_metrics, "tracked_keywords"),
            "tracked_competitors": _first_numeric(
                competitor_metrics, "tracked_competitors"
            ),
            "referring_domains": _first_numeric(backlink_metrics, "referring_domains"),
            "top_10_share": _first_numeric(rank_metrics, "top_10_share"),
            "product_modes": [
                "repo_methodology",
                "seo_intelligence_lab",
                "app_control_panel",
                "scanner_intake",
                "service_builder",
            ],
            "ci_first_class": True,
            "brand_queries_supported": "google_ads" in integration_metrics
            or "yandex_direct" in integration_metrics,
            "non_brand_queries_supported": "gsc" in integration_metrics
            or "yandex_webmaster" in integration_metrics,
            "crux_field_data_available": "crux" in integration_metrics
            and bool(crux_metrics),
        },
        executive_layers=executive_layers,
        comparison_metrics=comparison_metrics,
        benchmark_overlays=benchmark_overlays,
        anomalies=anomalies,
        owner_suggestions=owner_suggestions,
        operating_queue=operating_queue,
        portfolio_view=portfolio_view,
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
