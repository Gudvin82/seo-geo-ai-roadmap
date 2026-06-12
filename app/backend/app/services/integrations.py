from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from .script_runner import run_script


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
    if source == "gsc":
        code, stdout, stderr = run_script("gsc_data_stub.py", [])
        if code != 0:
            raise RuntimeError(stderr or "GSC starter import failed.")
        return json.loads(stdout)
    if source == "ga4":
        return _ga4_stub()
    if source == "yandex_webmaster":
        code, stdout, stderr = run_script("yandex_data_stub.py", [])
        if code != 0:
            raise RuntimeError(stderr or "Yandex Webmaster starter import failed.")
        return json.loads(stdout)
    if source == "yandex_metrica":
        return _yandex_metrica_stub()
    raise ValueError(f"Unsupported integration source '{source_type}'.")


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
