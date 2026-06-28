from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a lightweight SERP competitor matrix from intent lanes."
    )
    parser.add_argument("keywords", nargs="+", help="Keywords to cluster")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    rows = []
    for keyword in args.keywords:
        lane = (
            "commercial"
            if any(token in keyword.lower() for token in ["best", "agency", "service"])
            else "informational"
        )
        rows.append(
            {
                "keyword": keyword,
                "intent_lane": lane,
                "competitor_gap": "proof" if lane == "commercial" else "faq_depth",
                "recommended_asset": (
                    "comparison page or case pack"
                    if lane == "commercial"
                    else "answer-ready support article"
                ),
            }
        )
    payload = {"rows": rows, "keyword_count": len(rows)}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# SERP Competitor Matrix\n")
    for row in rows:
        print(f"- {row['keyword']}: {row['intent_lane']} -> {row['recommended_asset']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
