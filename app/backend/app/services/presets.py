from __future__ import annotations

AUDIT_PRESETS = {
    "local_business": [
        "robots_ai_bots",
        "sitemap",
        "llms_txt",
        "content_freshness",
        "local_yandex_readiness",
    ],
    "legal_compliance_website": [
        "robots_ai_bots",
        "llms_txt",
        "factual_consistency",
        "content_freshness",
        "hallucination_framework",
    ],
    "technical_product_site": [
        "robots_ai_bots",
        "sitemap",
        "llms_txt",
        "ai_sov_starter",
        "entity_hierarchy_review",
    ],
    "personal_expert_brand": [
        "factual_consistency",
        "hallucination_framework",
        "entity_hierarchy_review",
        "content_freshness",
    ],
    "global_multilingual": [
        "robots_ai_bots",
        "sitemap",
        "llms_txt",
        "factual_consistency",
        "content_freshness",
        "entity_hierarchy_review",
    ],
}
