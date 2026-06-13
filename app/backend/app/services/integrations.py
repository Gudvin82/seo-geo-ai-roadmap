from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from .script_runner import run_script

CONTRACT_VERSION = "v4.1.0"

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
}


def integration_contract(source_type: str) -> dict[str, Any]:
    source = source_type.strip().lower()
    if source not in INTEGRATION_CONTRACTS:
        raise ValueError(f"Unsupported integration source '{source_type}'.")
    return {
        **INTEGRATION_CONTRACTS[source],
        "contract_version": CONTRACT_VERSION,
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


def sync_integration_source(source_type: str) -> dict[str, Any]:
    source = source_type.strip().lower()
    contract = integration_contract(source)
    if source == "gsc":
        code, stdout, stderr = run_script("gsc_data_stub.py", [])
        if code != 0:
            raise RuntimeError(stderr or "GSC starter import failed.")
        payload = json.loads(stdout)
    elif source == "ga4":
        payload = _ga4_stub()
    elif source == "yandex_webmaster":
        code, stdout, stderr = run_script("yandex_data_stub.py", [])
        if code != 0:
            raise RuntimeError(stderr or "Yandex Webmaster starter import failed.")
        payload = json.loads(stdout)
    elif source == "yandex_metrica":
        payload = _yandex_metrica_stub()
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
