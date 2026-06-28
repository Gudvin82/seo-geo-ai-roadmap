#!/usr/bin/env python3
"""Cluster keywords into semantic execution lanes."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "your",
    "best",
    "how",
    "what",
    "why",
    "guide",
    "services",
    "service",
    "price",
    "pricing",
    "agency",
    "seo",
    "geo",
    "ai",
    "audit",
    "tool",
    "tools",
    "in",
    "on",
    "to",
    "of",
    "a",
}

INTENT_RULES = {
    "commercial": {"price", "pricing", "cost", "agency", "service", "services"},
    "informational": {"how", "what", "guide", "checklist", "template", "examples"},
    "transactional": {"buy", "demo", "contact", "hire", "book", "order"},
    "navigational": {"login", "docs", "github", "brand", "official"},
}


def normalize_tokens(keyword: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Zа-яА-Я0-9]+", keyword.lower())]


def detect_intent(tokens: list[str]) -> str:
    for intent, triggers in INTENT_RULES.items():
        if any(token in triggers for token in tokens):
            return intent
    return "mixed"


def cluster_key(tokens: list[str]) -> str:
    filtered = [token for token in tokens if token not in STOP_WORDS]
    if not filtered:
        return "general_visibility"
    return "_".join(filtered[:2])


def suggested_page_type(intent: str) -> str:
    return {
        "commercial": "service_or_comparison_page",
        "informational": "guide_or_faq_page",
        "transactional": "landing_or_demo_page",
        "navigational": "brand_or_help_page",
        "mixed": "hub_page",
    }[intent]


def load_keywords(args: argparse.Namespace) -> list[str]:
    if args.keyword:
        return args.keyword
    if args.file:
        return [
            line.strip()
            for line in Path(args.file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    return []


def build_payload(keywords: list[str]) -> dict[str, object]:
    clusters: dict[str, dict[str, object]] = {}
    funnel_counts = defaultdict(int)
    for keyword in keywords:
        tokens = normalize_tokens(keyword)
        intent = detect_intent(tokens)
        funnel_counts[intent] += 1
        key = cluster_key(tokens)
        row = clusters.setdefault(
            key,
            {
                "cluster": key,
                "intent": intent,
                "keywords": [],
                "recommended_page_type": suggested_page_type(intent),
                "recommended_actions": [],
            },
        )
        row["keywords"].append(keyword)

    for row in clusters.values():
        intent = row["intent"]
        if intent == "commercial":
            row["recommended_actions"] = [
                "compare offer clarity, proof density, and CTA strength",
                "build or upgrade service/comparison page coverage",
            ]
        elif intent == "informational":
            row["recommended_actions"] = [
                "publish a definitive explainer with FAQ and sources",
                "link the guide to a relevant service or product outcome",
            ]
        elif intent == "transactional":
            row["recommended_actions"] = [
                "shorten the conversion path and strengthen trust blocks",
                "test form, demo, or contact CTA clarity",
            ]
        else:
            row["recommended_actions"] = [
                "keep brand/help pages aligned with core facts",
                "reduce ambiguity and add obvious next steps",
            ]

    return {
        "tracked_keywords": len(keywords),
        "cluster_count": len(clusters),
        "intent_mix": dict(funnel_counts),
        "clusters": list(clusters.values()),
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Semantic Gap Map",
        "",
        f"- tracked_keywords: `{payload['tracked_keywords']}`",
        f"- cluster_count: `{payload['cluster_count']}`",
        "",
        "| Cluster | Intent | Recommended page type | Sample keywords |",
        "|---|---|---|---|",
    ]
    for row in payload["clusters"]:
        keywords = ", ".join(row["keywords"][:3])
        lines.append(
            f"| {row['cluster']} | {row['intent']} | {row['recommended_page_type']} | {keywords} |"
        )
    lines.extend(["", "## Intent mix", ""])
    for intent, count in payload["intent_mix"].items():
        lines.append(f"- {intent}: {count}")
    lines.extend(
        [
            "",
            "## Recommended next step",
            "",
            "Turn each cluster into a page owner, page type, and proof requirement before writing content.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map keywords into semantic clusters and execution lanes."
    )
    parser.add_argument("--keyword", action="append", help="Keyword to include.")
    parser.add_argument("--file", help="Path to a newline-delimited keyword file.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    keywords = load_keywords(args)
    if not keywords:
        raise SystemExit("Provide --keyword or --file with at least one keyword.")
    payload = build_payload(keywords)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
