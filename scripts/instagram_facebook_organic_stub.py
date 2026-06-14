#!/usr/bin/env python3
"""Emit a starter Instagram or Facebook organic analytics shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "instagram-facebook-organic-stub",
        "note": "Replace with a real Instagram or Facebook organic integration later.",
        "profiles": [
            {
                "handle": "@discoverability.os",
                "followers": 9800,
                "reach": 22100,
                "engagement_rate": 0.041,
                "site_clicks": 63,
            }
        ],
        "metrics": {
            "followers": 9800,
            "reach": 22100,
            "engagement_rate": 0.041,
            "site_clicks": 63,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
