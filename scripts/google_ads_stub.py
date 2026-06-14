#!/usr/bin/env python3
"""Emit a starter Google Ads shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "google-ads-stub",
        "note": "Replace with a real Google Ads API integration later.",
        "campaigns": [
            {
                "campaign": "Brand Search",
                "ad_group": "Brand Core",
                "search_term": "discoverability os",
                "clicks": 118,
                "impressions": 1420,
                "ctr": 0.083,
                "cost": 184.6,
                "conversions": 14,
                "cpa": 13.19,
            }
        ],
        "metrics": {
            "cost": 184.6,
            "conversions": 14,
            "ctr": 0.083,
            "cpa": 13.19,
            "cpl": 18.46,
            "brand_share_of_demand": 0.58,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
