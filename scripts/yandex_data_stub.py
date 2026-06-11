#!/usr/bin/env python3
"""Emit a starter Yandex Webmaster shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "yandex-stub",
        "note": "Replace with a real Yandex integration later.",
        "dimensions": ["query", "page", "region", "device"],
        "rows": [
            {
                "query": "geo аудит сайта",
                "page": "https://example.com/geo-audit",
                "clicks": 27,
                "impressions": 340,
                "ctr": 0.079,
                "position": 6.2,
            }
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
