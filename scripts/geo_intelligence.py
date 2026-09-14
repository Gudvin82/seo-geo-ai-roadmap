#!/usr/bin/env python3
"""CLI adapter for the same GEO runtime used by the FastAPI application."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._runtime_bootstrap import bootstrap_backend_imports  # noqa: E402

bootstrap_backend_imports()

from app.services.geo_intelligence import (  # noqa: E402
    RUNNERS,
    build_agent_audit_pack,
    build_geo_runtime,
    evidence,
    finding,
)


def load_observations(path: str | None) -> list[dict]:
    if not path:
        return []
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = (
        payload.get("observations", payload) if isinstance(payload, dict) else payload
    )
    observations = []
    for index, row in enumerate(rows, start=1):
        category = str(row.get("category") or row.get("component") or "citation")
        value = float(row.get("value", 50))
        observations.append(
            finding(
                category=category,
                observation=row.get(
                    "finding", row.get("claim", f"Observation {index}")
                ),
                recommendation=row.get(
                    "recommendation",
                    "Validate evidence and prepare an approved remediation task.",
                ),
                severity="high" if value < 40 else "medium" if value < 70 else "low",
                priority={
                    "impact": 3,
                    "effort": 2,
                    "score": round(100 - value),
                    "label": "review",
                },
                evidence_items=[
                    evidence(
                        observation=row.get(
                            "claim", row.get("finding", f"Observation {index}")
                        ),
                        source=row.get("source", "operator"),
                        evidence_type=row.get("evidence_type", "manual-review"),
                        confidence=float(row.get("confidence", 0.5)),
                        verification_method=row.get(
                            "verification_method", "operator input"
                        ),
                        reference=row.get("reference", ""),
                    )
                ],
            )
        )
    return observations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the application GEO Intelligence runtime from JSON evidence."
    )
    parser.add_argument(
        "command",
        choices=[
            "audit",
            "score",
            "entity",
            "citation",
            "authority",
            "competitor",
            "roadmap",
            "monitor",
            "doctor",
        ],
    )
    parser.add_argument("target", nargs="?", default="https://example.com")
    parser.add_argument(
        "--input", help="JSON observations; this command never fetches a URL directly."
    )
    parser.add_argument("--profile", default="default-v1")
    parser.add_argument(
        "--weights", help="Optional JSON object overriding a validated profile."
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    if args.command == "doctor":
        print(
            json.dumps(
                {
                    "status": "ready",
                    "runtime": "app.services.geo_intelligence",
                    "agent_pack": build_agent_audit_pack(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if not urlparse(args.target).scheme:
        raise SystemExit("Target must be an absolute URL.")
    observations = load_observations(args.input)
    if args.command in RUNNERS:
        result = RUNNERS[args.command](observations)
    else:
        runtime = build_geo_runtime(
            observations,
            args.profile,
            json.loads(args.weights) if args.weights else None,
        )
        result = (
            runtime
            if args.command != "roadmap"
            else {"roadmap": runtime["roadmap"], "scorecard": runtime["scorecard"]}
        )
    if args.format == "markdown":
        print(
            f"# GEO runtime: {args.target}\n\n```json\n{json.dumps(result, ensure_ascii=False, indent=2)}\n```"
        )
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
