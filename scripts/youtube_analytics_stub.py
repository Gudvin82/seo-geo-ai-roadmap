#!/usr/bin/env python3
"""Emit a starter YouTube analytics shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "youtube-analytics-stub",
        "note": "Replace with a real YouTube Analytics integration later.",
        "videos": [
            {
                "title": "AI visibility audit demo",
                "views": 1820,
                "watch_time_hours": 96.4,
                "click_through_rate": 0.054,
                "site_clicks": 38,
            }
        ],
        "metrics": {
            "views": 1820,
            "watch_time_hours": 96.4,
            "site_clicks": 38,
            "subscriber_growth": 47,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
