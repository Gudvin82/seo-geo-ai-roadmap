#!/usr/bin/env python3
"""Emit a starter Reddit mentions payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "reddit-mentions-stub",
        "note": "Replace with live Reddit mention tracking or approved social monitoring later.",
        "mentions": [
            {
                "community": "r/seo",
                "topic": "AI discoverability tooling",
                "mentions": 5,
                "sentiment": "mixed",
                "site_clicks": 9,
            },
            {
                "community": "r/entrepreneur",
                "topic": "Self-hosted audit stack",
                "mentions": 3,
                "sentiment": "positive",
                "site_clicks": 6,
            },
        ],
        "metrics": {
            "communities": 2,
            "mentions": 8,
            "site_clicks": 15,
            "positive_mentions": 3,
        },
        "opportunities": [
            "answer repeated community questions with product proof",
            "turn positive mention threads into public case-study evidence",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
