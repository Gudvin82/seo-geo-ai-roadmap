from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from .script_runner import run_script

CONTRACT_VERSION = "v4.2.0"

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


def sync_integration_source(
    source_type: str,
    *,
    property_identifier: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
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
    return {
        "id": source_type,
        "surface_type": "integration",
        "surface_name": label,
        "source_type": source_type,
        "readiness_tier": contract["readiness_tier"],
        "proof_level": proof_level,
        "credentials_status": "configured" if credentials_env_var else "missing",
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
        "next_step": contract["next_step"],
    }
