#!/usr/bin/env python3
"""Emit a starter Meta Ads shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "meta-ads-stub",
        "note": "Replace with a real Meta Ads integration later.",
        "campaigns": [
            {
                "campaign": "Remarketing",
                "spend": 96.3,
                "clicks": 84,
                "ctr": 0.027,
                "leads": 6,
                "cpl": 16.05,
            }
        ],
        "metrics": {
            "spend": 96.3,
            "leads": 6,
            "ctr": 0.027,
            "cpl": 16.05,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
