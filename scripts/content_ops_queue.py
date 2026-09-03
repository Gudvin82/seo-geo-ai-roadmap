#!/usr/bin/env python3
"""Turn semantic demand into an approval-first content operations queue.

This is a planning tool. It does not publish, rewrite, or claim that a task
will improve rankings or AI citations. Operators supply demand and evidence,
then use the output as a reviewable editorial backlog.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class QueueItem:
    topic: str
    intent: str
    page_type: str
    demand: int
    business_value: int
    evidence_strength: int
    effort: int
    score: int
    priority: str
    owner: str
    stage: str
    required_gates: list[str]
    next_step: str


INTENT_PAGE_TYPES = {
    "commercial": "service_or_comparison_page",
    "informational": "guide_or_faq_page",
    "transactional": "landing_or_demo_page",
    "navigational": "brand_or_help_page",
}

GATES = [
    "intent and audience review",
    "source and factual-claim review",
    "internal-link and canonical review",
    "editorial and legal approval",
    "post-publish verification",
]


def bounded_int(value: str, field: str, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an integer") from exc
    if not minimum <= parsed <= maximum:
        raise ValueError(f"{field} must be between {minimum} and {maximum}")
    return parsed


def queue_score(
    demand: int, business_value: int, evidence_strength: int, effort: int
) -> int:
    """Return an explainable 0-100 planning score, not a performance forecast."""
    weighted = demand * 0.35 + business_value * 0.35 + evidence_strength * 0.2
    effort_penalty = effort * 0.1
    return max(0, min(100, round(weighted - effort_penalty)))


def priority_for(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


def build_item(row: dict[str, str], default_owner: str) -> QueueItem:
    topic = row.get("topic", "").strip()
    if not topic:
        raise ValueError("topic is required")
    intent = row.get("intent", "mixed").strip().lower()
    page_type = row.get("page_type", "").strip() or INTENT_PAGE_TYPES.get(
        intent, "hub_page"
    )
    demand = bounded_int(row.get("demand", "0"), "demand", 0, 100)
    business_value = bounded_int(
        row.get("business_value", "50"), "business_value", 0, 100
    )
    evidence_strength = bounded_int(
        row.get("evidence_strength", "50"), "evidence_strength", 0, 100
    )
    effort = bounded_int(row.get("effort", "50"), "effort", 0, 100)
    score = queue_score(demand, business_value, evidence_strength, effort)
    return QueueItem(
        topic=topic,
        intent=intent,
        page_type=page_type,
        demand=demand,
        business_value=business_value,
        evidence_strength=evidence_strength,
        effort=effort,
        score=score,
        priority=priority_for(score),
        owner=row.get("owner", "").strip() or default_owner,
        stage="brief_required",
        required_gates=GATES,
        next_step="Create a brief; do not publish until every required gate is approved.",
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_payload(rows: list[dict[str, str]], default_owner: str) -> dict[str, object]:
    items = sorted(
        (build_item(row, default_owner) for row in rows),
        key=lambda item: (-item.score, item.topic.lower()),
    )
    return {
        "schema_version": "v6.9.5",
        "mode": "approval_first_content_operations",
        "task_count": len(items),
        "items": [asdict(item) for item in items],
        "boundary": "Planning score is not a ranking, traffic, conversion, or citation forecast.",
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Content Operations Queue",
        "",
        f"- mode: `{payload['mode']}`",
        f"- task_count: `{payload['task_count']}`",
        "- publication: `approval required`",
        "",
        "| Priority | Topic | Intent | Page type | Score | Owner | Stage |",
        "|---|---|---|---|---:|---|---|",
    ]
    for item in payload["items"]:
        lines.append(
            "| {priority} | {topic} | {intent} | {page_type} | {score} | {owner} | {stage} |".format(
                **item
            )
        )
    lines.extend(
        [
            "",
            "## Required Gates",
            "",
            *[f"- {gate}" for gate in GATES],
            "",
            "## Boundary",
            "",
            str(payload["boundary"]),
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an approval-first content operations queue from a CSV file."
    )
    parser.add_argument(
        "--file", required=True, help="CSV with topic and scoring inputs."
    )
    parser.add_argument("--default-owner", default="content_operator")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    try:
        payload = build_payload(load_rows(Path(args.file)), args.default_owner)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
