from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from .script_runner import run_script

CONTRACT_VERSION = "v5.1.0"

INTEGRATION_CONTRACTS: dict[str, dict[str, Any]] = {
    "gsc": {
        "source_type": "gsc",
        "label": "Google Search Console",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GSC_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "scheduled sync",
            "artifact export",
            "drift comparison",
            "report regeneration",
        ],
        "production_flow": [
            "connect service account secret",
            "run first manual sync",
            "review imported snapshot",
            "promote to scheduled GitHub Action or scheduled check",
            "use executive dashboard and compare flows for regression gating",
        ],
        "capabilities": [
            "top queries import",
            "top pages import",
            "search visibility baseline",
            "report attachment",
        ],
        "next_step": "Connect a service account secret, sync manually once, then move it into GitHub Actions or scheduled checks.",
    },
    "ga4": {
        "source_type": "ga4",
        "label": "Google Analytics 4",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GA4_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "landing-page validation",
            "engagement trend export",
            "delivery pack regeneration",
        ],
        "production_flow": [
            "connect GA4 credential secret",
            "validate baseline metrics import",
            "bind to project executive dashboard",
            "re-run after major content or release changes",
        ],
        "capabilities": [
            "sessions import",
            "engagement import",
            "top-page metrics",
            "executive dashboard rollup",
        ],
        "next_step": "Use GA4 as the executive outcome layer after core crawlability and discoverability signals are stable.",
    },
    "google_ads": {
        "source_type": "google_ads",
        "label": "Google Ads",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "campaign baseline refresh",
            "search-term drift review",
            "brand vs non-brand split review",
            "cost-to-conversion validation",
        ],
        "production_flow": [
            "connect Google Ads credentials",
            "sync campaigns, ad groups, and search terms",
            "separate brand and non-brand demand",
            "compare paid demand with organic and AI visibility",
        ],
        "capabilities": [
            "campaign import",
            "ad group import",
            "search terms import",
            "cost and conversion tracking",
            "brand vs non-brand demand context",
        ],
        "next_step": "Use Google Ads as the paid-demand layer paired with GSC and GA4 for full-funnel search interpretation.",
    },
    "yandex_webmaster": {
        "source_type": "yandex_webmaster",
        "label": "Yandex Webmaster",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_WEBMASTER_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "RU indexation baseline",
            "regional diagnostics refresh",
            "artifact export",
        ],
        "production_flow": [
            "connect Yandex Webmaster token",
            "validate RU property mapping",
            "schedule recurring sync for regional visibility checks",
            "attach RU findings to deliverables and dashboard",
        ],
        "capabilities": [
            "top queries import",
            "top pages import",
            "regional discoverability baseline",
            "RU deliverable support",
        ],
        "next_step": "Treat Yandex Webmaster as a first-class RU market source and keep it in the same recurring comparison loop as GSC.",
    },
    "yandex_metrica": {
        "source_type": "yandex_metrica",
        "label": "Yandex Metrica",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_METRICA_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "traffic sanity checks",
            "goal trend export",
            "executive dashboard refresh",
        ],
        "production_flow": [
            "connect Yandex Metrica token",
            "verify visits and goals import",
            "pair analytics with Yandex Webmaster diagnostics",
            "track post-fix performance deltas in executive mode",
        ],
        "capabilities": [
            "visit import",
            "goal conversion import",
            "top-page metrics",
            "RU executive dashboard support",
        ],
        "next_step": "Use Metrica as the RU engagement and conversion layer paired with Yandex Webmaster for indexation and diagnostics.",
    },
    "yandex_direct": {
        "source_type": "yandex_direct",
        "label": "Yandex Direct",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_DIRECT_TOKEN"],
        "recommended_ci_workflow": ".github/workflows/ai-visibility-check.yml",
        "ci_gates": [
            "campaign baseline refresh",
            "brand-demand drift review",
            "landing-page alignment check",
            "cost-to-discoverability comparison",
        ],
        "production_flow": [
            "connect Yandex Direct token",
            "pull campaign and ad-group baseline",
            "compare paid demand with organic and AI discoverability shifts",
            "use spend and conversion context in executive and delivery packs",
        ],
        "capabilities": [
            "campaign baseline import",
            "brand-demand context",
            "paid-vs-organic comparison",
            "landing-page alignment support",
        ],
        "next_step": "Use Yandex Direct as the paid-demand companion to Yandex Webmaster and Metrica when RU acquisition quality matters.",
    },
    "indexnow": {
        "source_type": "indexnow",
        "label": "IndexNow",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_push",
        "required_env_vars": ["INDEXNOW_KEY"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "fresh-url push",
            "submission success review",
            "indexation delta verification",
        ],
        "production_flow": [
            "configure IndexNow key",
            "submit changed URLs in batches",
            "verify acceptance rate",
            "compare post-submit indexation with GSC and Webmaster",
        ],
        "capabilities": [
            "fresh URL submission",
            "batch diagnostics",
            "indexation acceleration support",
        ],
        "next_step": "Use IndexNow as the fast-change distribution layer for pages that need fresher discovery signals.",
    },
    "google_business_profile": {
        "source_type": "google_business_profile",
        "label": "Google Business Profile",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["GBP_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "rating refresh",
            "review trend review",
            "local action validation",
        ],
        "production_flow": [
            "connect profile credentials",
            "sync ratings, reviews, and local actions",
            "compare profile demand with local landing performance",
            "attach local proof to executive and client outputs",
        ],
        "capabilities": [
            "ratings and reviews import",
            "calls and direction-request context",
            "local SEO proof support",
        ],
        "next_step": "Use Google Business Profile whenever local intent, maps demand, or trust signals affect conversion.",
    },
    "yandex_business": {
        "source_type": "yandex_business",
        "label": "Yandex Business",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YANDEX_BUSINESS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "map visibility refresh",
            "review trend review",
            "route-build and click validation",
        ],
        "production_flow": [
            "connect Yandex Business token",
            "sync maps reviews and local actions",
            "compare local RU demand with landing-page performance",
            "use results in RU executive and local-service delivery",
        ],
        "capabilities": [
            "rating and review import",
            "maps action context",
            "RU local SEO proof support",
        ],
        "next_step": "Use Yandex Business alongside Webmaster and Metrica when local RU intent matters.",
    },
    "merchant_center": {
        "source_type": "merchant_center",
        "label": "Google Merchant Center",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["MERCHANT_CENTER_SERVICE_ACCOUNT_JSON"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "feed health review",
            "product approval-rate review",
            "top issue export",
        ],
        "production_flow": [
            "connect Merchant Center credentials",
            "sync product feed diagnostics",
            "compare feed health with landing and conversion performance",
            "track approval-rate regressions over time",
        ],
        "capabilities": [
            "feed diagnostics import",
            "product approval tracking",
            "e-commerce issue visibility",
        ],
        "next_step": "Use Merchant Center for e-commerce properties where feed health affects discoverability and conversions.",
    },
    "crux": {
        "source_type": "crux",
        "label": "Chrome UX Report",
        "readiness_tier": "production_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["CRUX_API_KEY"],
        "recommended_ci_workflow": ".github/workflows/lighthouse-ci.yml",
        "ci_gates": [
            "field data refresh",
            "core web vitals regression check",
            "executive dashboard refresh",
        ],
        "production_flow": [
            "connect CrUX API key",
            "bind an origin or URL to the integration config",
            "compare field data against synthetic checks",
            "use scheduled refresh for release and post-fix verification",
        ],
        "capabilities": [
            "real-user CWV field data",
            "origin or URL scope tracking",
            "executive dashboard support",
            "release regression context",
        ],
        "next_step": "Use CrUX as the field-data layer that complements synthetic audits and release gating.",
    },
    "meta_ads": {
        "source_type": "meta_ads",
        "label": "Meta Ads",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["META_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "retargeting baseline refresh",
            "lead cost review",
            "landing alignment check",
        ],
        "production_flow": [
            "connect Meta Ads token",
            "sync campaign spend and lead data",
            "compare retargeting efficiency with organic and AI demand",
            "use as a paid amplification layer, not core SEO truth",
        ],
        "capabilities": [
            "campaign spend import",
            "lead and CPL tracking",
            "retargeting context",
        ],
        "next_step": "Use Meta Ads as a paid amplification and remarketing layer, not as a substitute for search data.",
    },
    "vk_ads": {
        "source_type": "vk_ads",
        "label": "VK Ads",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["VK_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "RU campaign baseline refresh",
            "lead cost review",
            "landing alignment review",
        ],
        "production_flow": [
            "connect VK Ads token",
            "sync spend clicks and leads",
            "compare RU paid demand with Webmaster and Direct",
            "use it as a RU growth layer around the core search stack",
        ],
        "capabilities": [
            "campaign spend import",
            "lead and CPL tracking",
            "RU paid distribution context",
        ],
        "next_step": "Use VK Ads when RU paid acquisition and community demand need to be measured next to search channels.",
    },
    "telegram_ads": {
        "source_type": "telegram_ads",
        "label": "Telegram Ads or Channel Analytics",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["TELEGRAM_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "reach baseline refresh",
            "click and lead review",
            "channel demand validation",
        ],
        "production_flow": [
            "connect Telegram ads or channel analytics token",
            "sync channel reach clicks and leads",
            "compare channel demand with landing conversion",
            "use it as a community and distribution signal layer",
        ],
        "capabilities": [
            "channel reach import",
            "click tracking",
            "community demand context",
        ],
        "next_step": "Use Telegram when your distribution model depends on channels, communities, or post-driven demand.",
    },
    "youtube": {
        "source_type": "youtube",
        "label": "YouTube Analytics",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["YOUTUBE_ANALYTICS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "video performance refresh",
            "site-click review",
            "channel growth validation",
        ],
        "production_flow": [
            "connect YouTube Analytics token",
            "sync video and channel performance",
            "compare media demand with branded search and citations",
            "use it as a discoverability and content-distribution layer",
        ],
        "capabilities": [
            "video metrics import",
            "watch-time context",
            "site-click tracking",
        ],
        "next_step": "Use YouTube where educational video or branded media affects search and AI demand.",
    },
    "linkedin_ads": {
        "source_type": "linkedin_ads",
        "label": "LinkedIn Ads",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["LINKEDIN_ADS_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "B2B campaign refresh",
            "lead cost review",
            "landing alignment review",
        ],
        "production_flow": [
            "connect LinkedIn Ads token",
            "sync spend clicks and lead data",
            "compare B2B demand with branded search and conversion paths",
            "use it as a B2B amplification layer",
        ],
        "capabilities": [
            "campaign spend import",
            "lead and CPL tracking",
            "B2B distribution context",
        ],
        "next_step": "Use LinkedIn Ads for B2B acquisition where paid awareness shapes search and conversion demand.",
    },
    "instagram_facebook_organic": {
        "source_type": "instagram_facebook_organic",
        "label": "Instagram or Facebook Organic",
        "readiness_tier": "distribution_guided",
        "sync_mode": "manual_or_scheduled_pull",
        "required_env_vars": ["META_GRAPH_TOKEN"],
        "recommended_ci_workflow": "examples/github-actions/ai-visibility-check.yml",
        "ci_gates": [
            "reach baseline refresh",
            "engagement trend review",
            "site-click validation",
        ],
        "production_flow": [
            "connect Meta Graph token",
            "sync reach engagement and site-click data",
            "compare organic social demand with brand demand and conversion",
            "use it as a supporting content-distribution signal",
        ],
        "capabilities": [
            "reach import",
            "engagement tracking",
            "site-click context",
        ],
        "next_step": "Use Instagram or Facebook organic data as a supporting distribution signal, not as the core SEO or GEO layer.",
    },
}


def integration_contract(source_type: str) -> dict[str, Any]:
    source = source_type.strip().lower()
    if source not in INTEGRATION_CONTRACTS:
        raise ValueError(f"Unsupported integration source '{source_type}'.")
    return {
        **INTEGRATION_CONTRACTS[source],
        "contract_version": CONTRACT_VERSION,
    }


def integration_env_status(contract: dict[str, Any]) -> dict[str, Any]:
    required = contract.get("required_env_vars", [])
    present = [name for name in required if os.getenv(name, "").strip()]
    missing = [name for name in required if name not in present]
    return {
        "required_env_vars": required,
        "present_env_vars": present,
        "missing_env_vars": missing,
        "live_credentials_ready": not missing,
    }


def all_integration_contracts() -> list[dict[str, Any]]:
    return [integration_contract(key) for key in sorted(INTEGRATION_CONTRACTS)]


def _ga4_stub() -> dict[str, Any]:
    return {
        "source": "ga4-stub",
        "note": "Starter analytics payload. Replace with a real GA4 API connector.",
        "metrics": {
            "sessions": 1240,
            "engaged_sessions": 841,
            "engagement_rate": 0.678,
            "avg_session_duration_seconds": 132,
        },
        "top_pages": [
            {"page": "/ai-visibility", "sessions": 320, "engagement_rate": 0.71},
            {"page": "/seo-audit", "sessions": 240, "engagement_rate": 0.66},
        ],
    }


def _yandex_metrica_stub() -> dict[str, Any]:
    return {
        "source": "yandex-metrica-stub",
        "note": "Starter analytics payload. Replace with a real Yandex Metrica connector.",
        "metrics": {
            "visits": 910,
            "users": 704,
            "bounce_rate": 0.28,
            "goal_completion_rate": 0.063,
        },
        "top_pages": [
            {"page": "/geo-audit", "visits": 190, "bounce_rate": 0.23},
            {"page": "/pricing", "visits": 130, "bounce_rate": 0.31},
        ],
    }


def _run_json_script(script_name: str, error_message: str) -> dict[str, Any]:
    code, stdout, stderr = run_script(script_name, [])
    if code != 0:
        raise RuntimeError(stderr or error_message)
    return json.loads(stdout)


def sync_integration_source(
    source_type: str,
    *,
    property_identifier: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = source_type.strip().lower()
    contract = integration_contract(source)
    if source == "gsc":
        payload = _run_json_script("gsc_data_stub.py", "GSC starter import failed.")
    elif source == "ga4":
        payload = _ga4_stub()
    elif source == "google_ads":
        payload = _run_json_script(
            "google_ads_stub.py", "Google Ads starter import failed."
        )
    elif source == "yandex_webmaster":
        payload = _run_json_script(
            "yandex_data_stub.py", "Yandex Webmaster starter import failed."
        )
    elif source == "yandex_metrica":
        payload = _yandex_metrica_stub()
    elif source == "yandex_direct":
        payload = _run_json_script(
            "yandex_direct_stub.py", "Yandex Direct starter import failed."
        )
    elif source == "indexnow":
        payload = _run_json_script("indexnow_stub.py", "IndexNow starter failed.")
    elif source == "google_business_profile":
        payload = _run_json_script(
            "google_business_profile_stub.py",
            "Google Business Profile starter import failed.",
        )
    elif source == "yandex_business":
        payload = _run_json_script(
            "yandex_business_stub.py", "Yandex Business starter import failed."
        )
    elif source == "merchant_center":
        payload = _run_json_script(
            "merchant_center_stub.py", "Merchant Center starter import failed."
        )
    elif source == "crux":
        target_url = (
            (config or {}).get("url") or property_identifier or "https://example.com/"
        )
        api_key = os.environ.get("CRUX_API_KEY", "").strip()
        if api_key:
            code, stdout, stderr = run_script(
                "crux_field_data.py", ["--url", target_url, "--json"]
            )
            if code == 0:
                payload = json.loads(stdout)
            else:
                payload = {
                    "source": "crux-starter-fallback",
                    "note": stderr
                    or "CrUX live import failed; returning starter fallback.",
                    "target_url": target_url,
                    "metrics": {},
                }
        else:
            payload = {
                "source": "crux-starter",
                "note": "CRUX_API_KEY is missing; returning starter payload.",
                "target_url": target_url,
                "metrics": {
                    "largest_contentful_paint": {"p75": 2800},
                    "interaction_to_next_paint": {"p75": 240},
                    "cumulative_layout_shift": {"p75": 0.12},
                },
            }
    elif source == "meta_ads":
        payload = _run_json_script("meta_ads_stub.py", "Meta Ads starter failed.")
    elif source == "vk_ads":
        payload = _run_json_script("vk_ads_stub.py", "VK Ads starter failed.")
    elif source == "telegram_ads":
        payload = _run_json_script(
            "telegram_ads_stub.py", "Telegram ads starter failed."
        )
    elif source == "youtube":
        payload = _run_json_script(
            "youtube_analytics_stub.py", "YouTube analytics starter failed."
        )
    elif source == "linkedin_ads":
        payload = _run_json_script(
            "linkedin_ads_stub.py", "LinkedIn Ads starter failed."
        )
    elif source == "instagram_facebook_organic":
        payload = _run_json_script(
            "instagram_facebook_organic_stub.py",
            "Instagram or Facebook organic starter failed.",
        )
    else:
        raise ValueError(f"Unsupported integration source '{source_type}'.")

    payload["contract"] = contract
    payload["sync_mode"] = contract["sync_mode"]
    payload["imported_at"] = datetime.utcnow().isoformat() + "Z"
    return payload


def compact_integration_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    rows = snapshot.get("rows") or []
    if rows:
        return {
            "row_count": len(rows),
            "top_queries": [row.get("query") for row in rows[:3]],
            "top_pages": [row.get("page") for row in rows[:3]],
            "imported_at": datetime.utcnow().isoformat() + "Z",
        }
    top_pages = snapshot.get("top_pages") or []
    metrics = snapshot.get("metrics") or {}
    return {
        "row_count": len(top_pages),
        "top_pages": [row.get("page") for row in top_pages[:3]],
        "metrics": metrics,
        "imported_at": datetime.utcnow().isoformat() + "Z",
    }


def _integration_proof_level(source_type: str, snapshot: dict[str, Any]) -> str:
    source = str(snapshot.get("source") or "").lower()
    if not snapshot:
        return "contract_only"
    if "stub" in source or "starter" in source or "fallback" in source:
        return "starter_or_stub"
    if source_type == "crux" and snapshot.get("metrics"):
        return "live_or_sampled_metrics"
    return "live_api_or_runtime"


def build_integration_verification_row(
    source_type: str,
    *,
    label: str,
    credentials_env_var: str | None = None,
    property_identifier: str | None = None,
    latest_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contract = integration_contract(source_type)
    snapshot = latest_snapshot or {}
    proof_level = _integration_proof_level(source_type, snapshot)
    env_status = integration_env_status(contract)
    return {
        "id": source_type,
        "surface_type": "integration",
        "surface_name": label,
        "source_type": source_type,
        "readiness_tier": contract["readiness_tier"],
        "proof_level": proof_level,
        "credentials_status": "configured"
        if credentials_env_var or env_status["live_credentials_ready"]
        else "missing",
        "property_identifier": property_identifier,
        "ci_workflow": contract["recommended_ci_workflow"],
        "ci_gates": contract["ci_gates"],
        "capabilities": contract["capabilities"],
        "production_flow": contract["production_flow"],
        "verification_checks": [
            "credentials configured",
            "manual sync completed",
            "snapshot imported",
            "CI or scheduled refresh defined",
            "evidence attached to executive output",
        ],
        "latest_snapshot_source": snapshot.get("source"),
        "latest_snapshot_summary": compact_integration_summary(snapshot)
        if snapshot
        else {},
        "env_status": env_status,
        "next_step": contract["next_step"],
    }
