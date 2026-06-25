"""Emit a starter keyword research payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "keyword-research-starter",
        "metrics": {
            "tracked_keywords": 128,
            "brand_share": 0.31,
            "non_brand_share": 0.69,
            "high_intent_keywords": 22,
            "opportunity_keywords": 37,
            "query_cluster_coverage": 0.58,
        },
        "rows": [
            {
                "keyword": "seo geo ai audit",
                "intent": "commercial_investigation",
                "volume": 350,
                "difficulty_band": "medium",
                "current_coverage": "partial",
            },
            {
                "keyword": "ai citation score",
                "intent": "informational",
                "volume": 260,
                "difficulty_band": "medium",
                "current_coverage": "strong",
            },
            {
                "keyword": "yandex alice ai visibility",
                "intent": "commercial_investigation",
                "volume": 110,
                "difficulty_band": "low",
                "current_coverage": "missing",
            },
        ],
        "clusters": [
            "technical seo",
            "geo and ai visibility",
            "ru market and yandex",
            "local business visibility",
        ],
        "opportunities": [
            "build more non-brand comparison pages around GEO and AI visibility",
            "separate RU Yandex/Alice demand into its own landing cluster",
            "connect FAQ and trust-block content to high-intent commercial queries",
        ],
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
