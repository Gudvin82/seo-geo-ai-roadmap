from __future__ import annotations

from fastapi import APIRouter

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
        ],
        "glossary": ["GLOSSARY.md", "GLOSSARY_RU.md"],
        "agents": ["AGENTS.md"],
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
