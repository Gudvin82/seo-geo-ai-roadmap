"""Canonical product capability registry.

This registry is intentionally conservative. A capability is not marked
``production_ready`` merely because a contract, UI card, or starter script
exists. The generated matrix is used by the public API, docs, and CI.
"""

from __future__ import annotations

from typing import Any

from .integrations import all_integration_contracts

CAPABILITY_LEVELS = (
    "production_ready",
    "connected",
    "foundation",
    "stub",
)

LEVEL_BOUNDARIES = {
    "production_ready": "Implemented, tested in the self-hosted runtime, and safe to operate within documented limits.",
    "connected": "Uses the running application runtime but still depends on operator configuration or an external service.",
    "foundation": "Contracts and controlled paths exist; operator-owned end-to-end proof is still required.",
    "stub": "Shape-only starter payload or scaffold. It is not live data or a production connector.",
}

CORE_CAPABILITIES = (
    {
        "id": "scanner",
        "label": "Self-hosted URL scanner",
        "level": "production_ready",
        "surface": "runtime",
        "evidence": "scanner job tests and authenticated result access controls",
        "boundary": "A self-hosted operator owns deployment, rate limits, and target authorization.",
    },
    {
        "id": "canonical_finding_evidence",
        "label": "Canonical Finding/Evidence model",
        "level": "production_ready",
        "surface": "runtime",
        "evidence": "GEO runtime, report, task, graph, and API integration tests",
        "boundary": "Evidence types preserve provenance; heuristic evidence is not provider verification.",
    },
    {
        "id": "unified_geo_report",
        "label": "Unified GEO Intelligence Report",
        "level": "production_ready",
        "surface": "runtime",
        "evidence": "project-audit and scanner adapter report tests",
        "boundary": "The report explains readiness and evidence; it does not guarantee rankings or AI citations.",
    },
    {
        "id": "geo_cli",
        "label": "geo audit / score / roadmap / monitor CLI",
        "level": "connected",
        "surface": "cli",
        "evidence": "CLI smoke test plus API-backed endpoint tests",
        "boundary": "Requires a running self-hosted app and the appropriate scanner session or API token.",
    },
    {
        "id": "score_calibration",
        "label": "Readiness-score calibration",
        "level": "foundation",
        "surface": "methodology",
        "evidence": "dated consented-data calibration utility and validation tests",
        "boundary": "No validated external benchmark exists until an adequate independent dataset is supplied.",
    },
    {
        "id": "ai_visibility_monitoring",
        "label": "AI visibility history",
        "level": "foundation",
        "surface": "runtime",
        "evidence": "provider evidence snapshot contracts and history storage",
        "boundary": "Provider-derived observations must be collected with an operator-authorized provider path.",
    },
)

LIVE_FOUNDATION_SOURCES = {
    "gsc",
    "yandex_webmaster",
    "crux",
    "indexnow",
    "keyword_research",
    "competitor_intelligence",
    "backlink_intelligence",
    "rank_tracking",
}


def _integration_row(contract: dict[str, Any]) -> dict[str, Any]:
    source_type = contract["source_type"]
    level = "foundation" if source_type in LIVE_FOUNDATION_SOURCES else "stub"
    is_foundation = level == "foundation"
    return {
        "id": f"integration:{source_type}",
        "label": contract["label"],
        "level": level,
        "surface": "integration",
        "source_type": source_type,
        "required_env_vars": contract["required_env_vars"],
        "capabilities": contract["capabilities"],
        "evidence": (
            "Runtime connector exists; provider credentials and operator-owned E2E proof are still required."
            if is_foundation
            else "Starter payload or operator-guided import path is shipped."
        ),
        "boundary": (
            "Do not claim a connected or production-ready integration without an operator-owned E2E proof record."
            if is_foundation
            else "No live provider data is returned by this repository without a future connector implementation."
        ),
    }


def product_capability_matrix() -> dict[str, Any]:
    """Return a machine-readable, evidence-bound product capability matrix."""
    rows = [dict(row) for row in CORE_CAPABILITIES]
    rows.extend(_integration_row(contract) for contract in all_integration_contracts())
    rows.sort(key=lambda row: (row["surface"], row["label"]))
    counts = {
        level: sum(row["level"] == level for row in rows) for level in CAPABILITY_LEVELS
    }
    return {
        "schema_version": "v1",
        "generated_from": "app.backend.app.services.capabilities",
        "levels": list(CAPABILITY_LEVELS),
        "level_boundaries": LEVEL_BOUNDARIES,
        "summary": {"total": len(rows), "by_level": counts},
        "rows": rows,
    }
