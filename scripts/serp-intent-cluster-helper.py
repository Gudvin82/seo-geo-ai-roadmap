#!/usr/bin/env python3
"""Create rough intent clusters from keywords."""

from __future__ import annotations

import argparse
from collections import defaultdict


def classify(keyword: str) -> str:
    text = keyword.lower()
    if any(token in text for token in ["buy", "price", "cost", "заказать", "цена"]):
        return "commercial"
    if any(token in text for token in ["best", "vs", "compare", "alternative", "лучший", "сравнение"]):
        return "comparison"
    if any(token in text for token in ["what is", "how", "guide", "что такое", "как"]):
        return "informational"
    return "mixed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Group keywords by rough search intent.")
    parser.add_argument("keywords", nargs="+", help="Keyword list")
    args = parser.parse_args()
    clusters: dict[str, list[str]] = defaultdict(list)
    for keyword in args.keywords:
        clusters[classify(keyword)].append(keyword)
    print("| Intent | Keywords |")
    print("|---|---|")
    for intent, keywords in clusters.items():
        print(f"| {intent} | {', '.join(keywords)} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
