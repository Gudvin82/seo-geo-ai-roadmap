#!/usr/bin/env python3
"""Emit a starter Dzen distribution payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "dzen-stub",
        "note": "Replace with a real Dzen analytics integration later.",
        "metrics": {
            "reach": 9800,
            "clicks": 144,
            "ctr": 0.036,
            "site_clicks": 52,
        },
        "topics": [
            {"topic": "AI visibility", "reach": 4200, "site_clicks": 19},
            {"topic": "Yandex trust blocks", "reach": 3100, "site_clicks": 14},
        ],
        "opportunities": [
            "turn the best Dzen topic into a long-form explainer page",
            "reuse top-performing Dzen intros for article openers",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
