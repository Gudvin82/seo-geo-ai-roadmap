"""Emit a starter rank tracking payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "rank-tracking-starter",
        "metrics": {
            "tracked_queries": 42,
            "top_3_share": 0.21,
            "top_10_share": 0.54,
            "visibility_delta_30d": 0.08,
            "serp_feature_capture_rate": 0.19,
        },
        "rows": [
            {
                "query": "seo geo ai platform",
                "current_position": 4,
                "previous_position": 6,
                "movement": "+2",
                "serp_features": ["snippet", "faq"],
            },
            {
                "query": "alice ai visibility",
                "current_position": 11,
                "previous_position": 14,
                "movement": "+3",
                "serp_features": ["ai_overview_candidate"],
            },
            {
                "query": "local seo yandex business",
                "current_position": 7,
                "previous_position": 5,
                "movement": "-2",
                "serp_features": ["maps"],
            },
        ],
        "opportunities": [
            "promote rising queries with stronger internal links and proof blocks",
            "improve pages sitting in positions 4 to 12 first",
            "separate SERP feature capture work from classic rank work in weekly ops",
        ],
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
