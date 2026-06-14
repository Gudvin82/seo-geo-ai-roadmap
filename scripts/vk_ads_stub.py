#!/usr/bin/env python3
"""Emit a starter VK Ads shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "vk-ads-stub",
        "note": "Replace with a real VK Ads integration later.",
        "campaigns": [
            {
                "campaign": "RU Demand Capture",
                "spend": 74.4,
                "clicks": 61,
                "ctr": 0.031,
                "leads": 5,
                "cpl": 14.88,
            }
        ],
        "metrics": {
            "spend": 74.4,
            "leads": 5,
            "ctr": 0.031,
            "cpl": 14.88,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
