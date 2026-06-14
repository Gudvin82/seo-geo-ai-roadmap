#!/usr/bin/env python3
"""Emit a starter Google Business Profile shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "google-business-profile-stub",
        "note": "Replace with a real Google Business Profile integration later.",
        "locations": [
            {
                "name": "Main office",
                "rating": 4.8,
                "reviews": 126,
                "phone_calls": 19,
                "direction_requests": 27,
                "website_clicks": 41,
            }
        ],
        "metrics": {
            "locations": 1,
            "average_rating": 4.8,
            "review_count": 126,
            "local_actions": 87,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
