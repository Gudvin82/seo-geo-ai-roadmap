#!/usr/bin/env python3
"""Emit a starter Yandex Business shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "yandex-business-stub",
        "note": "Replace with a real Yandex Business integration later.",
        "locations": [
            {
                "name": "Moscow office",
                "rating": 4.7,
                "reviews": 88,
                "map_views": 312,
                "route_builds": 22,
                "website_clicks": 29,
            }
        ],
        "metrics": {
            "locations": 1,
            "average_rating": 4.7,
            "review_count": 88,
            "map_actions": 363,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
