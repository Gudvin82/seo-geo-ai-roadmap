#!/usr/bin/env python3
"""Emit a starter GA4 shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "ga4-stub",
        "note": "Replace with a real GA4 Data API integration later.",
        "metrics": {
            "sessions": 1240,
            "engaged_sessions": 841,
            "engagement_rate": 0.678,
            "avg_session_duration_seconds": 132,
        },
        "top_pages": [
            {"page": "/ai-visibility", "sessions": 320, "engagement_rate": 0.71},
            {"page": "/seo-audit", "sessions": 240, "engagement_rate": 0.66},
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
