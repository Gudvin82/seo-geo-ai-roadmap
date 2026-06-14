#!/usr/bin/env python3
"""Emit a starter TikTok organic payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "tiktok-organic-stub",
        "note": "Replace with live TikTok analytics or approved exported data later.",
        "videos": [
            {
                "video": "3 GEO mistakes founders make",
                "views": 8700,
                "watch_rate": 0.36,
                "profile_clicks": 47,
                "site_clicks": 18,
            }
        ],
        "metrics": {
            "views": 8700,
            "watch_rate": 0.36,
            "profile_clicks": 47,
            "site_clicks": 18,
        },
        "opportunities": [
            "promote high-retention clips into landing page hooks",
            "turn top comments into FAQ and objection-handling copy",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
