#!/usr/bin/env python3
"""Emit a starter IndexNow shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "indexnow-stub",
        "note": "Replace with a real IndexNow ping and verification flow later.",
        "metrics": {
            "submitted_urls": 36,
            "accepted_urls": 34,
            "rejected_urls": 2,
            "success_rate": 0.944,
        },
        "recent_batches": [
            {"scope": "blog", "submitted": 12, "accepted": 12},
            {"scope": "services", "submitted": 24, "accepted": 22},
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
