#!/usr/bin/env python3
"""Emit a starter Telegram ads or channel analytics shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "telegram-ads-stub",
        "note": "Replace with a real Telegram ads or channel analytics integration later.",
        "channels": [
            {
                "channel": "@discoverability_os",
                "subscribers": 4200,
                "avg_post_reach": 1870,
                "clicks": 92,
                "leads": 4,
            }
        ],
        "metrics": {
            "subscribers": 4200,
            "avg_post_reach": 1870,
            "clicks": 92,
            "leads": 4,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
