#!/usr/bin/env python3
"""Emit a starter LinkedIn Ads shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "linkedin-ads-stub",
        "note": "Replace with a real LinkedIn Ads integration later.",
        "campaigns": [
            {
                "campaign": "B2B Demand",
                "spend": 143.2,
                "clicks": 57,
                "ctr": 0.018,
                "leads": 7,
                "cpl": 20.46,
            }
        ],
        "metrics": {
            "spend": 143.2,
            "leads": 7,
            "ctr": 0.018,
            "cpl": 20.46,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
