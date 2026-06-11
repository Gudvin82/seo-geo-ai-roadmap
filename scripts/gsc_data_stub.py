#!/usr/bin/env python3
"""Emit a starter Google Search Console shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "gsc-stub",
        "note": "Replace with a real Search Console API integration later.",
        "dimensions": ["query", "page", "country", "device"],
        "rows": [
            {
                "query": "seo ai visibility",
                "page": "https://example.com/ai-visibility",
                "clicks": 42,
                "impressions": 510,
                "ctr": 0.082,
                "position": 7.4,
            }
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
