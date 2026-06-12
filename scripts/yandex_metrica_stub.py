#!/usr/bin/env python3
"""Emit a starter Yandex Metrica shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "yandex-metrica-stub",
        "note": "Replace with a real Yandex Metrica API integration later.",
        "metrics": {
            "visits": 910,
            "users": 704,
            "bounce_rate": 0.28,
            "goal_completion_rate": 0.063,
        },
        "top_pages": [
            {"page": "/geo-audit", "visits": 190, "bounce_rate": 0.23},
            {"page": "/pricing", "visits": 130, "bounce_rate": 0.31},
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
