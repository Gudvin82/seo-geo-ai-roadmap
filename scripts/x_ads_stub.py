#!/usr/bin/env python3
"""Emit a starter X Ads shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "x-ads-stub",
        "note": "Replace with a real X Ads integration later.",
        "campaigns": [
            {
                "campaign": "Thought-leadership amplification",
                "spend": 88.2,
                "clicks": 96,
                "ctr": 0.029,
                "leads": 5,
                "cpl": 17.64,
            }
        ],
        "metrics": {
            "spend": 88.2,
            "clicks": 96,
            "ctr": 0.029,
            "leads": 5,
            "cpl": 17.64,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
