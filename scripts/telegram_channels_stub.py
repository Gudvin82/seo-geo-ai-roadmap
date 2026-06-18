#!/usr/bin/env python3
"""Emit a starter Telegram channel intelligence payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "telegram-channels-stub",
        "note": "Replace with a real Telegram channel analytics integration later.",
        "metrics": {
            "reach": 14100,
            "forwards": 214,
            "site_clicks": 96,
            "leads": 7,
        },
        "top_posts": [
            {
                "title": "Client before/after AI visibility case",
                "reach": 5300,
                "site_clicks": 41,
            },
            {
                "title": "How to fix Yandex trust gaps",
                "reach": 4100,
                "site_clicks": 26,
            },
        ],
        "opportunities": [
            "promote the highest-click Telegram post into a landing-page proof strip",
            "add a short objection section based on repeated channel replies",
            "package top Telegram posts into a founder-led content sequence",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
