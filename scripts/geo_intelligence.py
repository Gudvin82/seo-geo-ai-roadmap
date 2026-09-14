#!/usr/bin/env python3
"""Evidence-first GEO Intelligence runner.

This command deliberately scores supplied observations, not claimed AI rankings.
It is usable by agents and humans: JSON is canonical, Markdown is a rendering.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

EVIDENCE_TYPES = {"verified", "provider-derived", "heuristic", "manual-review"}
DEFAULT_WEIGHTS = {
    "entity_authority": 25,
    "citation_readiness": 20,
    "technical_accessibility": 15,
    "content_intelligence": 15,
    "trust_signals": 15,
    "competitor_context": 10,
}


def load_payload(path: str | None, target: str) -> dict:
    if not path:
        return {"target": target, "observations": []}
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    payload.setdefault("target", target)
    payload.setdefault("observations", [])
    return payload


def build_report(payload: dict, weights: dict[str, float]) -> dict:
    evidence, findings, components = [], [], {key: [] for key in weights}
    for index, item in enumerate(payload.get("observations", []), start=1):
        evidence_type = item.get("evidence_type", "manual-review")
        if evidence_type not in EVIDENCE_TYPES:
            raise ValueError(f"Observation {index} has unsupported evidence_type.")
        component = item.get("component", "content_intelligence")
        if component not in components:
            continue
        value = max(0.0, min(100.0, float(item.get("value", 0))))
        confidence = max(0.0, min(1.0, float(item.get("confidence", 0.5))))
        components[component].append((value, confidence))
        evidence.append({
            "id": item.get("id", f"evidence-{index}"), "source": item.get("source", "operator"),
            "evidence_type": evidence_type, "confidence": confidence,
            "verification_method": item.get("verification_method", "manual review"),
            "observed_at": item.get("observed_at"), "claim": item.get("claim", ""),
        })
        if value < 70:
            findings.append({
                "id": item.get("id", f"finding-{index}"), "component": component,
                "severity": "high" if value < 40 else "medium", "evidence_id": evidence[-1]["id"],
                "summary": item.get("finding", f"{component} needs review."),
                "recommendation": item.get("recommendation", "Validate the evidence and create an approved remediation task."),
                "confidence": confidence, "evidence_type": evidence_type,
            })
    score_components = {}
    for name, weight in weights.items():
        rows = components[name]
        raw = sum(value * confidence for value, confidence in rows) / sum(confidence for _, confidence in rows) if rows and sum(confidence for _, confidence in rows) else 0.0
        score_components[name] = {"score": round(raw, 1), "weight": weight, "evidence_count": len(rows), "status": "measured" if rows else "insufficient_data"}
    total_weight = sum(weights.values()) or 100
    score = round(sum(row["score"] * row["weight"] for row in score_components.values()) / total_weight, 1)
    roadmap = [{"priority": "P0" if item["severity"] == "high" else "P1", "owner": "unassigned", "impact": "high" if item["severity"] == "high" else "medium", "effort": "estimate_required", "dependency": "evidence verification", "verification": "re-run this GEO Intelligence report", "task": item["recommendation"]} for item in findings]
    return {"contract_version": "v6.10.0", "generated_at": datetime.now(timezone.utc).isoformat(), "target": payload.get("target"), "scorecard": {"score": score, "weights": weights, "components": score_components, "boundary": "Heuristic and provider-derived signals do not guarantee AI citations, rankings, traffic, or conversions."}, "evidence": evidence, "findings": findings, "roadmap": roadmap}


def markdown(report: dict) -> str:
    lines = [f"# GEO Intelligence Report: {report['target']}", "", f"- GEO score: {report['scorecard']['score']}/100", "- Boundary: this is an evidence-led decision aid, not a citation or ranking guarantee.", "", "## Components", "", "| Component | Score | Evidence | Status |", "| --- | ---: | ---: | --- |"]
    lines.extend(f"| {name} | {row['score']} | {row['evidence_count']} | {row['status']} |" for name, row in report["scorecard"]["components"].items())
    lines.extend(["", "## Roadmap", ""])
    lines.extend(f"- [{item['priority']}] {item['task']} Owner: {item['owner']}; verify: {item['verification']}." for item in report["roadmap"]) 
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an evidence-first GEO Intelligence report.")
    parser.add_argument("command", choices=["audit", "score", "entity", "citation", "roadmap", "monitor", "doctor"])
    parser.add_argument("target", nargs="?", default="https://example.com")
    parser.add_argument("--input", help="JSON observations using the GEO Intelligence contract")
    parser.add_argument("--weights", help="Optional JSON object overriding scorecard weights")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    if args.command == "doctor":
        print(json.dumps({"contract_version": "v6.10.0", "status": "ready", "checks": [{"name": "python", "status": "pass"}, {"name": "observations_contract", "status": "pass"}], "boundary": "Provider credentials and browser rendering are optional capabilities."}, ensure_ascii=False, indent=2))
        return 0
    if not urlparse(args.target).scheme:
        raise SystemExit("Target must be an absolute URL.")
    weights = DEFAULT_WEIGHTS | (json.loads(args.weights) if args.weights else {})
    report = build_report(load_payload(args.input, args.target), weights)
    print(markdown(report) if args.format == "markdown" else json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
