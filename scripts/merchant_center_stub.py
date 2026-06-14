#!/usr/bin/env python3
"""Emit a starter Merchant Center shaped payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "merchant-center-stub",
        "note": "Replace with a real Merchant Center integration later.",
        "metrics": {
            "products": 248,
            "approved_products": 231,
            "disapproved_products": 17,
            "approval_rate": 0.931,
            "feed_warnings": 9,
        },
        "top_issues": [
            "missing_gtin",
            "shipping_mismatch",
            "image_quality_warning",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
