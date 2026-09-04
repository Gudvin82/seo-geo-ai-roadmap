#!/usr/bin/env python3
"""Build a governed content lifecycle from demand exports and draft evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "v6.9.6"
TOKEN_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁ0-9]+")
REQUIRED_GATES = (
    "intent_review",
    "factual_review",
    "technical_review",
    "editorial_legal_approval",
    "post_publish_verification",
)


def tokens(value: str) -> set[str]:
    return {item.lower() for item in TOKEN_RE.findall(value) if len(item) > 2}


def overlap(left: str, right: str) -> float:
    left_tokens, right_tokens = tokens(left), tokens(right)
    union = left_tokens | right_tokens
    return len(left_tokens & right_tokens) / len(union) if union else 0.0


def read_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload if isinstance(payload, list) else payload.get("rows", [])
        if not isinstance(records, list):
            raise ValueError(f"{path}: JSON rows must be a list")
        return [dict(item) for item in records]
    with path.open(encoding="utf-8", newline="") as handle:
        return [dict(item) for item in csv.DictReader(handle)]


def number(row: dict[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return default


def normalize_demand(source: dict[str, Any], base: Path) -> list[dict[str, Any]]:
    source_type = str(source["type"]).lower()
    path = (base / str(source["file"])).resolve()
    rows = []
    for raw in read_records(path):
        query = str(
            raw.get("query") or raw.get("keyword") or raw.get("topic") or ""
        ).strip()
        if not query:
            continue
        impressions = number(raw, "impressions", "shows", "volume")
        clicks = number(raw, "clicks", "visits")
        position = number(raw, "position", "average_position", default=100.0)
        business_value = number(raw, "business_value", default=50.0)
        evidence = min(
            100.0, 30.0 + min(impressions, 10000.0) / 150.0 + min(clicks, 1000.0) / 20.0
        )
        demand = min(
            100.0, max(impressions / 100.0, clicks / 5.0, number(raw, "demand"))
        )
        rows.append(
            {
                "query": query,
                "source": source_type,
                "impressions": round(impressions),
                "clicks": round(clicks),
                "position": round(position, 2),
                "demand": round(demand),
                "business_value": round(min(100.0, business_value)),
                "evidence_strength": round(evidence),
                "source_file": str(path),
            }
        )
    return rows


def merge_demand(sources: list[dict[str, Any]], base: Path) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for source in sources:
        for row in normalize_demand(source, base):
            key = " ".join(sorted(tokens(row["query"]))) or row["query"].lower()
            current = merged.setdefault(
                key,
                {
                    "query": row["query"],
                    "sources": [],
                    "impressions": 0,
                    "clicks": 0,
                    "position": 100.0,
                    "demand": 0,
                    "business_value": 0,
                    "evidence_strength": 0,
                },
            )
            current["sources"].append(row["source"])
            current["impressions"] += row["impressions"]
            current["clicks"] += row["clicks"]
            current["position"] = min(current["position"], row["position"])
            current["demand"] = max(current["demand"], row["demand"])
            current["business_value"] = max(
                current["business_value"], row["business_value"]
            )
            current["evidence_strength"] = min(
                100,
                max(current["evidence_strength"], row["evidence_strength"])
                + 5 * (len(set(current["sources"])) - 1),
            )
    return sorted(merged.values(), key=lambda item: (-item["demand"], item["query"]))


def inspect_registry(
    demand: list[dict[str, Any]], registry: list[dict[str, Any]], threshold: float
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    conflicts, candidates = [], []
    for row in demand:
        matches = [
            {
                "url": item.get("url"),
                "cluster": item.get("cluster"),
                "overlap": round(
                    overlap(row["query"], str(item.get("cluster", ""))), 3
                ),
            }
            for item in registry
            if overlap(row["query"], str(item.get("cluster", ""))) >= threshold
        ]
        target = dict(row)
        if matches:
            target["registry_matches"] = matches
            target["recommended_action"] = "update_or_consolidate_existing_page"
            conflicts.append(target)
        else:
            target["recommended_action"] = "prepare_new_brief"
            candidates.append(target)
    return conflicts, candidates


def validate_draft(draft: dict[str, Any]) -> dict[str, Any]:
    checks = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"id": check_id, "passed": passed, "detail": detail})

    title = str(draft.get("title", ""))
    description = str(draft.get("meta_description", ""))
    slug = str(draft.get("slug", ""))
    headings = draft.get("headings", [])
    links = draft.get("internal_links", [])
    schemas = draft.get("schema_types", [])
    sources = draft.get("factual_sources", [])
    body = str(draft.get("body", ""))
    add("title", 20 <= len(title) <= 65, "title should be 20-65 characters")
    add(
        "meta_description",
        70 <= len(description) <= 170,
        "description should be 70-170 characters",
    )
    add(
        "slug",
        bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)),
        "slug must be lowercase ASCII with hyphens",
    )
    add(
        "h1",
        len([item for item in headings if item.get("level") == 1]) == 1,
        "exactly one H1 is required",
    )
    add("heading_depth", len(headings) >= 3, "use a meaningful answer structure")
    add("internal_links", len(links) >= 2, "at least two intentional internal links")
    add("schema", bool(schemas), "declare applicable schema types")
    add("factual_sources", len(sources) >= 1, "material claims need source records")
    add(
        "author",
        bool(str(draft.get("author", "")).strip()),
        "identify the accountable author or reviewer",
    )
    add("body", len(tokens(body)) >= 80, "draft needs substantive reviewed content")
    failures = [item for item in checks if not item["passed"]]
    return {
        "draft_id": draft.get("id") or slug,
        "status": "ready_for_human_approval" if not failures else "blocked",
        "checks": checks,
        "failure_count": len(failures),
        "required_gates": list(REQUIRED_GATES),
    }


def build_monitoring(
    previous: list[dict[str, Any]],
    current: list[dict[str, Any]],
    registry: list[dict[str, Any]],
) -> dict[str, Any]:
    old = {str(row.get("query")): row for row in previous}
    opportunities, deltas = [], []
    for row in current:
        query = str(row.get("query", ""))
        position = number(row, "position", default=100.0)
        previous_position = number(old.get(query, {}), "position", default=position)
        delta = round(previous_position - position, 2)
        deltas.append({"query": query, "position": position, "position_change": delta})
        if 4 <= position <= 15:
            opportunities.append(
                {
                    "query": query,
                    "position": position,
                    "position_change": delta,
                    "action": "review_existing_page_before_creating_new_content",
                }
            )
    return {
        "opportunities_4_15": opportunities,
        "position_deltas": deltas,
        "topic_inventory": len(registry),
        "monitoring_boundary": "Position changes are observations, not proof of causality.",
    }


def build_advisor(report: dict[str, Any], budget: dict[str, Any]) -> dict[str, Any]:
    max_items = max(1, min(int(budget.get("max_recommendations", 5)), 20))
    recommendations = []
    for item in report["cannibalization_conflicts"]:
        recommendations.append(
            {
                "priority": "high",
                "action": item["recommended_action"],
                "query": item["query"],
            }
        )
    for item in report["monitoring"]["opportunities_4_15"]:
        recommendations.append(
            {"priority": "medium", "action": item["action"], "query": item["query"]}
        )
    for item in report["draft_checks"]:
        if item["status"] == "blocked":
            recommendations.append(
                {
                    "priority": "high",
                    "action": "resolve_draft_quality_failures",
                    "draft_id": item["draft_id"],
                }
            )
    return {
        "mode": "deterministic_advisor_no_writeback",
        "recommendations": recommendations[:max_items],
        "budget": {
            "max_recommendations": max_items,
            "llm_calls_allowed": int(budget.get("llm_calls_allowed", 0)),
            "max_cost_usd": float(budget.get("max_cost_usd", 0)),
        },
        "safety": "Advisor cannot publish, modify CMS content, or approve its own recommendations.",
    }


def cover_svg(title: str, subtitle: str) -> str:
    safe_title, safe_subtitle = html.escape(title[:70]), html.escape(subtitle[:100])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="{safe_title}">
  <defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#06233f"/><stop offset="1" stop-color="#087f8c"/></linearGradient></defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <circle cx="1030" cy="80" r="250" fill="#5ef2c2" opacity=".16"/>
  <text x="80" y="265" fill="#ffffff" font-family="Georgia,serif" font-size="64">{safe_title}</text>
  <text x="82" y="340" fill="#c8fff0" font-family="Verdana,sans-serif" font-size="28">{safe_subtitle}</text>
  <text x="82" y="550" fill="#ffffff" opacity=".75" font-family="Verdana,sans-serif" font-size="20">Generated template - review brand, rights, and accessibility before publishing</text>
</svg>"""


def run(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base = manifest_path.parent
    demand = merge_demand(manifest.get("demand_sources", []), base)
    registry = read_records((base / manifest["registry_file"]).resolve())
    conflicts, candidates = inspect_registry(
        demand, registry, float(manifest.get("cannibalization_threshold", 0.5))
    )
    drafts = read_records((base / manifest["drafts_file"]).resolve())
    previous = read_records((base / manifest["previous_positions_file"]).resolve())
    current = read_records((base / manifest["current_positions_file"]).resolve())
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "demand": demand,
        "new_topic_candidates": candidates,
        "cannibalization_conflicts": conflicts,
        "draft_checks": [validate_draft(item) for item in drafts],
        "monitoring": build_monitoring(previous, current, registry),
        "knowledge_base": manifest.get("knowledge_base", {}),
        "publication_policy": "human_approval_required",
    }
    report["advisor"] = build_advisor(report, manifest.get("advisor_budget", {}))
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "content-lifecycle-report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    media = manifest.get("optional_media", {})
    if media.get("enabled"):
        (output_dir / "cover.svg").write_text(
            cover_svg(
                str(media.get("title", "Content update")),
                str(media.get("subtitle", "")),
            ),
            encoding="utf-8",
        )
    report["report_sha256"] = hashlib.sha256(report_path.read_bytes()).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the governed content lifecycle.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--format", choices=("json", "summary"), default="summary")
    args = parser.parse_args()
    try:
        report = run(Path(args.manifest).resolve(), Path(args.output_dir).resolve())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            "content-lifecycle-ok:"
            f"demand={len(report['demand'])}:"
            f"conflicts={len(report['cannibalization_conflicts'])}:"
            f"drafts={len(report['draft_checks'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
