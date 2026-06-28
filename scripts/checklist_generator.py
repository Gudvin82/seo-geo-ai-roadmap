#!/usr/bin/env python3
"""Generate a tailored SEO/GEO/AI checklist."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ChecklistItem:
    category: str
    priority: str
    title: str
    why: str
    owner: str
    market: str


COMMON_ITEMS: tuple[ChecklistItem, ...] = (
    ChecklistItem(
        category="technical_seo",
        priority="high",
        title="Verify indexable pages return 200 and canonical targets are intentional.",
        why="Technical discoverability is the floor for search and AI reuse.",
        owner="seo_operator",
        market="all",
    ),
    ChecklistItem(
        category="technical_seo",
        priority="high",
        title="Confirm robots.txt, sitemap.xml, and internal linking do not hide money pages.",
        why="Discovery and crawl flow must be explicit before higher-layer GEO work compounds.",
        owner="seo_operator",
        market="all",
    ),
    ChecklistItem(
        category="content",
        priority="high",
        title="Map each key intent to a dedicated landing, service, or explainer page.",
        why="Intent-to-page mapping is the base of semantic coverage and conversion clarity.",
        owner="content_lead",
        market="all",
    ),
    ChecklistItem(
        category="trust",
        priority="high",
        title="Strengthen proof blocks: cases, reviews, expert identity, offers, and legal clarity.",
        why="Trust surfaces help both ranking and AI summarization quality.",
        owner="brand_owner",
        market="all",
    ),
    ChecklistItem(
        category="geo_ai",
        priority="high",
        title="Audit answer-ready blocks, llms.txt/ai.txt posture, and factual consistency.",
        why="AI systems prefer extractable answers and consistent entity facts.",
        owner="geo_operator",
        market="all",
    ),
)

SITE_TYPE_ITEMS: dict[str, tuple[ChecklistItem, ...]] = {
    "service": (
        ChecklistItem(
            category="conversion",
            priority="high",
            title="Clarify service pages with who it is for, what changes, proof, and CTA.",
            why="Service businesses win when offer clarity and proof density are obvious.",
            owner="product_marketer",
            market="all",
        ),
    ),
    "saas": (
        ChecklistItem(
            category="product_marketing",
            priority="high",
            title="Differentiate feature pages, use cases, integrations, and pricing intent.",
            why="SaaS demand is split across product, comparison, and workflow queries.",
            owner="growth_pm",
            market="all",
        ),
    ),
    "local_business": (
        ChecklistItem(
            category="local",
            priority="high",
            title="Align NAP, maps entities, reviews, geo pages, and appointment/contact flows.",
            why="Local visibility depends on entity consistency and trust at the city or district level.",
            owner="local_seo_owner",
            market="all",
        ),
    ),
    "ecommerce": (
        ChecklistItem(
            category="commerce",
            priority="high",
            title="Review category intent, product schema, merchant trust, and feed hygiene.",
            why="Commercial queries require clean category logic and credible product data.",
            owner="commerce_operator",
            market="all",
        ),
    ),
    "media": (
        ChecklistItem(
            category="editorial",
            priority="medium",
            title="Maintain freshness, article clustering, author trust, and archive hygiene.",
            why="Media discoverability depends on coverage depth, recency, and author signals.",
            owner="editorial_lead",
            market="all",
        ),
    ),
}

MARKET_ITEMS: dict[str, tuple[ChecklistItem, ...]] = {
    "global": (
        ChecklistItem(
            category="ai_surfaces",
            priority="medium",
            title="Benchmark Google, ChatGPT, Perplexity, and Gemini answer behavior for target prompts.",
            why="Global GEO performance differs by provider and query class.",
            owner="geo_operator",
            market="global",
        ),
    ),
    "ru": (
        ChecklistItem(
            category="ru_market",
            priority="high",
            title="Validate Yandex Webmaster, Yandex Metrica, YandexAdditional, and Alice AI visibility posture.",
            why="RU discoverability requires explicit Yandex and Alice AI operating discipline.",
            owner="ru_growth_owner",
            market="ru",
        ),
        ChecklistItem(
            category="ru_market",
            priority="medium",
            title="Review legal/trust blocks, pricing clarity, regional signals, and local business entities for RU traffic.",
            why="Commercial and trust factors are especially visible in the RU market.",
            owner="ru_growth_owner",
            market="ru",
        ),
    ),
}

FOCUS_ITEMS: dict[str, tuple[ChecklistItem, ...]] = {
    "seo": (
        ChecklistItem(
            category="seo_depth",
            priority="high",
            title="Cluster semantic demand, compare competitors, and separate authority vs content gaps.",
            why="Classical SEO grows fastest when semantics, competitors, and authority are reviewed together.",
            owner="seo_strategist",
            market="all",
        ),
    ),
    "geo": (
        ChecklistItem(
            category="geo_ai",
            priority="high",
            title="Test quote-ready answers, explicit facts, FAQ coverage, and source-worthy case evidence.",
            why="GEO wins when the site is easy to cite, summarize, and trust.",
            owner="geo_operator",
            market="all",
        ),
    ),
    "social": (
        ChecklistItem(
            category="distribution",
            priority="medium",
            title="Map proof-worthy content into social surfaces such as Telegram, VK, X, Threads, and YouTube.",
            why="Distribution layers create brand/entity reinforcement beyond on-site content only.",
            owner="distribution_owner",
            market="all",
        ),
    ),
    "local": (
        ChecklistItem(
            category="local",
            priority="high",
            title="Track Google Business Profile, Yandex Business, 2GIS, and review-response hygiene.",
            why="Maps and entity listings drive local search and AI source inclusion.",
            owner="local_seo_owner",
            market="all",
        ),
    ),
}


def build_checklist(
    site_type: str, market: str, focuses: list[str]
) -> list[ChecklistItem]:
    items = list(COMMON_ITEMS)
    items.extend(SITE_TYPE_ITEMS.get(site_type, ()))
    items.extend(MARKET_ITEMS.get(market, ()))
    for focus in focuses:
        items.extend(FOCUS_ITEMS.get(focus, ()))
    return items


def render_markdown(
    site_type: str, market: str, focuses: list[str], items: list[ChecklistItem]
) -> str:
    lines = [
        f"# Tailored Checklist: {site_type}",
        "",
        f"- market: `{market}`",
        f"- focus: `{', '.join(focuses) if focuses else 'baseline'}`",
        "",
        "| Priority | Category | Action | Why | Owner |",
        "|---|---|---|---|---|",
    ]
    for item in items:
        lines.append(
            f"| {item.priority} | {item.category} | {item.title} | {item.why} | {item.owner} |"
        )
    lines.extend(
        [
            "",
            "## How to use",
            "",
            "1. Mark each line as done, blocked, or deferred.",
            "2. Convert high-priority gaps into backlog items first.",
            "3. Keep before/after evidence for anything that changes visibility, trust, or conversion.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a tailored SEO/GEO/AI checklist."
    )
    parser.add_argument(
        "--site-type",
        choices=sorted(SITE_TYPE_ITEMS),
        default="service",
        help="Primary business/site model.",
    )
    parser.add_argument(
        "--market",
        choices=sorted(MARKET_ITEMS),
        default="global",
        help="Primary market context.",
    )
    parser.add_argument(
        "--focus",
        action="append",
        choices=sorted(FOCUS_ITEMS),
        default=[],
        help="Add optional focus lanes such as seo, geo, local, or social.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items = build_checklist(args.site_type, args.market, args.focus)
    if args.format == "json":
        payload = {
            "site_type": args.site_type,
            "market": args.market,
            "focus": args.focus,
            "items": [asdict(item) for item in items],
        }
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    print(render_markdown(args.site_type, args.market, args.focus, items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
