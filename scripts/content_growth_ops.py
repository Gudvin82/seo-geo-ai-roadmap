from __future__ import annotations

import argparse
import json


def build_plan(vertical: str, market: str) -> dict:
    return {
        "vertical": vertical,
        "market": market,
        "pillars": [
            {
                "id": "site_architecture",
                "goal": "separate money pages, comparison pages, and answer-ready explainers",
                "deliverables": ["url map", "intent clusters", "internal linking notes"],
            },
            {
                "id": "programmatic_seo",
                "goal": "define safe repeatable page families without index bloat",
                "deliverables": ["template rules", "quality gates", "indexability guardrails"],
            },
            {
                "id": "schema_and_facts",
                "goal": "align entity facts, schema coverage, and FAQ answer blocks",
                "deliverables": ["schema coverage plan", "fact source map", "FAQ backlog"],
            },
        ],
        "operator_rule": (
            "Treat content growth as an architecture problem first, then a writing problem."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a content-growth ops plan.")
    parser.add_argument("--vertical", default="general")
    parser.add_argument("--market", default="global")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    payload = build_plan(args.vertical, args.market)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Content Growth Ops")
    print()
    print(f"- vertical: `{payload['vertical']}`")
    print(f"- market: `{payload['market']}`")
    print()
    for pillar in payload["pillars"]:
        print(f"## {pillar['id']}")
        print()
        print(f"- goal: {pillar['goal']}")
        print(f"- deliverables: {', '.join(pillar['deliverables'])}")
        print()
    print("## Operator Rule")
    print()
    print(payload["operator_rule"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
