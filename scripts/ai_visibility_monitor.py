#!/usr/bin/env python3
"""Persist provider or operator AI-visibility evidence without inventing results."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

QUERY_SETS = {"brand", "non-brand", "comparison", "category", "local"}
EVIDENCE_TYPES = {"verified", "provider-derived", "heuristic", "manual-review"}


def load(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(row: dict) -> None:
    missing = [key for key in ("target", "query_set", "provider", "model", "observed_at", "evidence_type", "result") if key not in row]
    if missing:
        raise ValueError(f"Missing required evidence fields: {', '.join(missing)}")
    if row["query_set"] not in QUERY_SETS or row["evidence_type"] not in EVIDENCE_TYPES:
        raise ValueError("Unsupported query_set or evidence_type.")


def summarize(rows: list[dict]) -> dict:
    for row in rows:
        validate(row)
    mentions = sum(1 for row in rows if bool((row.get("result") or {}).get("mentioned")))
    return {"contract_version": "v6.11.0", "observed_at": datetime.now(timezone.utc).isoformat(), "records": len(rows), "mentions": mentions, "coverage": round(mentions / len(rows), 3) if rows else 0.0, "providers": sorted({row["provider"] for row in rows}), "query_sets": sorted({row["query_set"] for row in rows}), "boundary": "Records are evidence snapshots. Coverage is not a guarantee of future AI answers, rankings, traffic, or conversion."}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an AI Visibility Scenario Monitor summary.")
    parser.add_argument("input", help="JSON list of provider or operator evidence records")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    report = summarize(load(args.input))
    if args.format == "markdown":
        print(f"# AI Visibility Scenario Monitor\n\n- Evidence records: {report['records']}\n- Mention coverage: {report['coverage']}\n- Providers: {', '.join(report['providers']) or 'n/a'}\n- Boundary: {report['boundary']}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
