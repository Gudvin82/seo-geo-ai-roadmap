from __future__ import annotations

import argparse
import json


def build_pack(audience: str) -> dict:
    return {
        "audience": audience,
        "research_tracks": [
            {
                "id": "voice_of_customer",
                "sources": ["sales calls", "support chats", "reviews", "public forums"],
                "output": "objection and phrase library",
            },
            {
                "id": "competitor_comparisons",
                "sources": ["comparison pages", "search snippets", "AI answers"],
                "output": "why-us vs alternatives map",
            },
            {
                "id": "proof_harvest",
                "sources": [
                    "case notes",
                    "metrics",
                    "screenshots",
                    "operator artifacts",
                ],
                "output": "quote-safe proof inventory",
            },
        ],
        "operator_rule": (
            "Prefer direct customer language over generic marketing copy when shaping pages and prompts."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a customer-research pack.")
    parser.add_argument("--audience", default="site owners")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    payload = build_pack(args.audience)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Customer Research Pack")
    print()
    print(f"- audience: `{payload['audience']}`")
    print()
    for track in payload["research_tracks"]:
        print(f"## {track['id']}")
        print()
        print(f"- sources: {', '.join(track['sources'])}")
        print(f"- output: {track['output']}")
        print()
    print("## Operator Rule")
    print()
    print(payload["operator_rule"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
