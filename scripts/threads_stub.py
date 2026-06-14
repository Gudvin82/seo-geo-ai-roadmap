#!/usr/bin/env python3
"""Emit a starter Threads shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "threads-stub",
        "note": "Replace with live Threads profile and post analytics later.",
        "threads": [
            {
                "topic": "AI visibility myths",
                "views": 3600,
                "engagements": 144,
                "replies": 29,
                "site_clicks": 12,
            }
        ],
        "metrics": {
            "views": 3600,
            "engagements": 144,
            "replies": 29,
            "site_clicks": 12,
        },
        "opportunities": [
            "expand best discussion into a long-form explainer",
            "capture repeated objections for sales enablement",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
