"""Emit a starter backlink intelligence payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "backlink-intelligence-starter",
        "metrics": {
            "referring_domains": 84,
            "high_quality_referring_domains": 19,
            "lost_referring_domains_30d": 4,
            "new_referring_domains_30d": 6,
            "authority_trend": 0.12,
        },
        "rows": [
            {
                "domain": "industry-publication.example",
                "type": "editorial",
                "status": "live",
                "quality_band": "high",
            },
            {
                "domain": "local-directory.example",
                "type": "local_citation",
                "status": "lost",
                "quality_band": "medium",
            },
            {
                "domain": "partner-case.example",
                "type": "case_study",
                "status": "new",
                "quality_band": "high",
            },
        ],
        "opportunities": [
            "recover lost local and entity citations",
            "turn proof packs into editorial backlink targets",
            "prioritize high-trust domains that reinforce entity and GEO relevance",
        ],
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
