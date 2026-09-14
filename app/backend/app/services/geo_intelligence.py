"""Canonical GEO Intelligence runtime.

This module is deliberately data-first: it converts observations from existing
audits and providers into one finding/evidence contract.  It does not claim
that heuristic observations are provider-verified AI citations.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

CONTRACT_VERSION = "v1"
EVIDENCE_TYPES = {"verified", "provider-derived", "heuristic", "manual-review"}
ANALYZERS = ("entity", "citation", "authority", "competitor")
SCORE_PROFILES = {
    "default-v1": {
        "version": "v1",
        "calibration": "unvalidated",
        "weights": {
            "entity": 0.25,
            "citation": 0.25,
            "authority": 0.25,
            "competitor": 0.25,
        },
    },
    "ru-local-v1": {
        "version": "v1",
        "calibration": "unvalidated",
        "weights": {
            "entity": 0.30,
            "citation": 0.20,
            "authority": 0.30,
            "competitor": 0.20,
        },
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_weights(weights: dict[str, Any]) -> dict[str, float]:
    if set(weights) != set(ANALYZERS):
        raise ValueError(
            "Score weights must specify entity, citation, authority, and competitor."
        )
    normalized = {key: float(value) for key, value in weights.items()}
    if any(value < 0 for value in normalized.values()) or sum(normalized.values()) <= 0:
        raise ValueError(
            "Score weights must be non-negative and have a positive total."
        )
    total = sum(normalized.values())
    return {key: value / total for key, value in normalized.items()}


def resolve_score_profile(
    name: str = "default-v1", override: dict[str, Any] | None = None
) -> dict[str, Any]:
    if name not in SCORE_PROFILES:
        raise ValueError(f"Unknown score profile: {name}")
    profile = deepcopy(SCORE_PROFILES[name])
    profile["name"] = name
    if override is not None:
        profile["weights"] = validate_weights(override)
        profile["version"] = f"{profile['version']}+override"
    else:
        profile["weights"] = validate_weights(profile["weights"])
    return profile


def evidence(
    *,
    observation: str,
    source: str,
    evidence_type: str = "heuristic",
    confidence: float = 0.5,
    verification_method: str = "deterministic rule",
    reference: str = "",
) -> dict[str, Any]:
    if evidence_type not in EVIDENCE_TYPES:
        raise ValueError(f"Unsupported evidence_type: {evidence_type}")
    return {
        "id": f"evidence-{uuid4().hex}",
        "observation": observation,
        "source": source,
        "evidence_type": evidence_type,
        "confidence": max(0.0, min(float(confidence), 1.0)),
        "timestamp": utc_now(),
        "verification_method": verification_method,
        "reference": reference,
    }


def finding(
    *,
    category: str,
    observation: str,
    recommendation: str,
    priority: dict[str, Any],
    evidence_items: list[dict[str, Any]],
    severity: str = "medium",
) -> dict[str, Any]:
    if not evidence_items:
        evidence_items = [
            evidence(
                observation="No source evidence was supplied.",
                source="runtime",
                evidence_type="manual-review",
                confidence=0.0,
                verification_method="operator review required",
            )
        ]
    first = evidence_items[0]
    return {
        "id": f"finding-{uuid4().hex}",
        "contract_version": CONTRACT_VERSION,
        "category": category,
        "observation": observation,
        "evidence": evidence_items,
        "source": first["source"],
        "evidence_type": first["evidence_type"],
        "confidence": round(
            sum(item["confidence"] for item in evidence_items) / len(evidence_items), 2
        ),
        "timestamp": utc_now(),
        "verification_method": first["verification_method"],
        "recommendation": recommendation,
        "priority": priority,
        "severity": severity,
        # Compatibility keys retained for existing report/task/graph readers.
        "title": category.replace("_", " ").title(),
        "summary": observation,
        "impact": priority.get("impact"),
        "effort": priority.get("effort"),
        "priority_score": priority.get("score"),
        "priority_label": priority.get("label"),
    }


def normalize_finding(row: dict[str, Any]) -> dict[str, Any]:
    """Adapt legacy persisted findings without fabricating verified evidence."""
    if row.get("contract_version") == CONTRACT_VERSION and row.get("evidence"):
        return row
    priority = {
        "impact": row.get("impact", 3),
        "effort": row.get("effort", 3),
        "score": row.get("priority_score", 0),
        "label": row.get("priority_label", "review"),
    }
    return finding(
        category=row.get("category", "discoverability"),
        observation=row.get(
            "observation",
            row.get("summary", row.get("title", "Finding requires review.")),
        ),
        recommendation=row.get(
            "recommendation", "Review the finding and prepare a verified fix."
        ),
        priority=priority,
        severity=row.get("severity", "medium"),
        evidence_items=[
            evidence(
                observation=row.get("summary", row.get("title", "Legacy finding")),
                source=row.get("source", "legacy_audit_run"),
                evidence_type="heuristic",
                confidence=min(float(row.get("confidence", 3)) / 5, 1.0),
                verification_method="legacy audit adapter",
                reference=row.get("notes", ""),
            )
        ],
    )


_ANALYZER_KEYWORDS = {
    "entity": ("entity", "local_yandex"),
    "citation": ("citation", "robots", "sitemap", "llms", "ai_sov", "hallucination"),
    "authority": ("factual", "hallucination", "content_freshness"),
    "competitor": ("competitor",),
}


def _component(analyzer: str, observations: list[dict[str, Any]]) -> dict[str, Any]:
    related = [
        item
        for item in observations
        if any(
            keyword in str(item.get("category", ""))
            for keyword in _ANALYZER_KEYWORDS[analyzer]
        )
    ]
    if not related:
        return {
            "analyzer": analyzer,
            "status": "insufficient_data",
            "score": None,
            "findings": [],
        }
    normalized = [normalize_finding(item) for item in related]
    values = [
        max(0.0, min(100.0, 100.0 - float(item["priority"].get("score", 0))))
        for item in normalized
    ]
    return {
        "analyzer": analyzer,
        "status": "scored",
        "score": round(sum(values) / len(values), 2),
        "findings": normalized,
    }


def run_entity_analyzer(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return _component("entity", observations)


def run_citation_analyzer(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return _component("citation", observations)


def run_authority_analyzer(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return _component("authority", observations)


def run_competitor_analyzer(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return _component("competitor", observations)


RUNNERS = {
    "entity": run_entity_analyzer,
    "citation": run_citation_analyzer,
    "authority": run_authority_analyzer,
    "competitor": run_competitor_analyzer,
}


def calculate_score(
    components: dict[str, dict[str, Any]], profile: dict[str, Any]
) -> dict[str, Any]:
    scored = {
        name: value for name, value in components.items() if value["score"] is not None
    }
    coverage = sum(profile["weights"][name] for name in scored)
    if not scored:
        return {
            "status": "insufficient_data",
            "score": None,
            "coverage": 0.0,
            "unscored_weight": 1.0,
            "profile": profile,
        }
    weighted = sum(
        value["score"] * profile["weights"][name] for name, value in scored.items()
    )
    return {
        "status": "partial" if coverage < 1 else "scored",
        "score": round(weighted / coverage, 2),
        "coverage": round(coverage, 2),
        "unscored_weight": round(1 - coverage, 2),
        "profile": profile,
    }


def build_geo_runtime(
    observations: list[dict[str, Any]],
    profile_name: str = "default-v1",
    weights: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profile = resolve_score_profile(profile_name, weights)
    components = {name: runner(observations) for name, runner in RUNNERS.items()}
    findings = [
        item for component in components.values() for item in component["findings"]
    ]
    score = calculate_score(components, profile)
    roadmap = [
        {
            "finding_id": item["id"],
            "recommendation": item["recommendation"],
            "priority": item["priority"],
        }
        for item in sorted(
            findings,
            key=lambda row: float(row["priority"].get("score", 0)),
            reverse=True,
        )
    ]
    return {
        "contract_version": CONTRACT_VERSION,
        "generated_at": utc_now(),
        "components": components,
        "findings": findings,
        "scorecard": score,
        "roadmap": roadmap,
    }


def build_agent_audit_pack() -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "roles": ["operator", "audit-agent", "reviewer"],
        "tools": ["scanner", "geo_analyzers", "reports", "task_center"],
        "input": {
            "required": ["project_id", "target_url"],
            "optional": ["audit_run_id", "score_profile"],
        },
        "output": {"required": ["findings", "scorecard", "roadmap", "report", "tasks"]},
        "limits": {
            "no_unapproved_writeback": True,
            "no_secret_export": True,
            "evidence_required": True,
        },
        "sequence": ["audit", "analyze", "score", "roadmap", "report", "task"],
        "approval_gates": [
            "Any CMS writeback requires operator approval.",
            "Provider evidence must retain its provenance.",
        ],
    }


def normalize_scan_issue(issue: dict[str, Any], target_url: str) -> dict[str, Any]:
    """Adapt a scanner machine-report issue without changing scanner storage."""
    severity = str(issue.get("severity", "medium"))
    priority_score = {"critical": 90, "high": 80, "medium": 55, "low": 25}.get(
        severity, 40
    )
    category = str(issue.get("issue_id", "technical_seo"))
    return finding(
        category=category,
        observation=str(issue.get("title") or issue.get("summary") or "Scanner issue."),
        recommendation=str(
            issue.get("recommended_action")
            or "Review the scanner evidence and prepare an approved fix."
        ),
        priority={"impact": 4, "effort": 2, "score": priority_score, "label": severity},
        severity=severity,
        evidence_items=[
            evidence(
                observation=str(issue.get("title") or "Scanner issue."),
                source="scanner_machine_report",
                evidence_type="verified",
                confidence=0.8,
                verification_method="bounded scanner fetch and deterministic rule",
                reference=target_url,
            )
        ],
    )


def _section(findings: list[dict[str, Any]], *keywords: str) -> list[dict[str, Any]]:
    return [
        item
        for item in findings
        if any(keyword in str(item.get("category", "")).lower() for keyword in keywords)
    ]


def build_unified_report(
    *,
    target_url: str,
    findings: list[dict[str, Any]],
    scorecard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Produce the product-level report from the canonical finding contract."""
    canonical = [normalize_finding(item) for item in findings]
    if scorecard is None:
        scorecard = build_geo_runtime(canonical)["scorecard"]
    roadmap = [
        {
            "finding_id": item["id"],
            "action": item["recommendation"],
            "priority": item["priority"],
            "verification": item["verification_method"],
        }
        for item in sorted(
            canonical,
            key=lambda item: float(item["priority"].get("score", 0)),
            reverse=True,
        )
    ]
    return {
        "contract_version": CONTRACT_VERSION,
        "report_type": "geo_intelligence_unified",
        "generated_at": utc_now(),
        "target_url": target_url,
        "executive_summary": {
            "finding_count": len(canonical),
            "score_status": scorecard.get("status", "insufficient_data"),
            "score": scorecard.get("score"),
            "boundary": "Evidence types preserve provenance and do not guarantee rankings, AI citations, traffic, or conversions.",
        },
        "geo_score": scorecard,
        "technical_seo": _section(
            canonical, "robots", "sitemap", "canonical", "schema", "crawl", "meta"
        ),
        "entity_intelligence": _section(canonical, "entity", "local", "brand"),
        "citation_readiness": _section(canonical, "citation", "llms", "ai_", "robots"),
        "authority_signals": _section(
            canonical, "authority", "factual", "content", "trust"
        ),
        "ai_visibility": _section(canonical, "citation", "ai_", "hallucination"),
        "competitor_gap": _section(canonical, "competitor"),
        "evidence": [evidence for item in canonical for evidence in item["evidence"]],
        "recommended_actions": roadmap[:10],
        "roadmap": roadmap,
        "findings": canonical,
        "verification_plan": [
            "Apply only approved fixes.",
            "Re-run the same audit and compare source-labelled evidence.",
            "Record provider-derived observations as snapshots, not guarantees.",
        ],
    }


def render_unified_markdown(report: dict[str, Any]) -> str:
    """Human-readable rendering of the JSON source-of-truth report."""
    summary = report["executive_summary"]
    lines = [
        f"# GEO Intelligence Report: {report['target_url']}",
        "",
        "## Executive Summary",
        "",
        f"- GEO score: {summary['score'] if summary['score'] is not None else 'insufficient_data'}",
        f"- Findings: {summary['finding_count']}",
        f"- Evidence boundary: {summary['boundary']}",
        "",
    ]
    sections = (
        ("Technical SEO", "technical_seo"),
        ("Entity Intelligence", "entity_intelligence"),
        ("Citation Readiness", "citation_readiness"),
        ("Authority Signals", "authority_signals"),
        ("AI Visibility", "ai_visibility"),
        ("Competitor Gap", "competitor_gap"),
    )
    for label, key in sections:
        lines.extend([f"## {label}", ""])
        rows = report[key]
        if not rows:
            lines.append("- insufficient_data")
        for item in rows:
            lines.append(f"- [{item['severity']}] {item['observation']}")
            lines.append(
                f"  Evidence: {item['evidence_type']} from {item['source']} ({item['confidence']})"
            )
            lines.append(f"  Action: {item['recommendation']}")
        lines.append("")
    lines.extend(["## Roadmap", ""])
    for item in report["roadmap"]:
        lines.append(f"- {item['action']} Verify: {item['verification']}")
    lines.extend(["", "## Verification", ""])
    lines.extend(f"- {item}" for item in report["verification_plan"])
    return "\n".join(lines) + "\n"
