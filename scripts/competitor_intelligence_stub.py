"""Emit a starter competitor intelligence payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "competitor-intelligence-starter",
        "metrics": {
            "tracked_competitors": 5,
            "content_gap_count": 14,
            "trust_gap_count": 7,
            "geo_gap_count": 6,
            "authority_overlap_score": 0.42,
        },
        "rows": [
            {
                "competitor": "competitor-a.example",
                "gap_type": "content",
                "surface": "comparison pages",
                "severity": "high",
            },
            {
                "competitor": "competitor-b.example",
                "gap_type": "trust",
                "surface": "case studies and proof",
                "severity": "medium",
            },
            {
                "competitor": "competitor-c.example",
                "gap_type": "geo",
                "surface": "answer-ready FAQ coverage",
                "severity": "high",
            },
        ],
        "opportunities": [
            "publish side-by-side service comparison pages",
            "expand proof assets and case-study density on money pages",
            "improve entity clarity and FAQ coverage where competitors are being cited",
        ],
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
