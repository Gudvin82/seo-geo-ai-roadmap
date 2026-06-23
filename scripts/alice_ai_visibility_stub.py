#!/usr/bin/env python3
"""Emit a starter Alice AI visibility payload."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "source": "alice-ai-visibility-stub",
        "note": (
            "Operator-reviewed weekly Alice AI visibility snapshot based on Yandex "
            "Webmaster exports. Replace with a managed import or approved export feed later."
        ),
        "metrics": {
            "share_of_voice": 0.11,
            "weekly_delta": 0.02,
            "query_coverage": 0.58,
            "queries_with_own_mentions": 7,
            "competitor_source_overlap": 4,
            "insufficient_data": False,
            "mention_band": "top_10",
        },
        "rows": [
            {
                "query": "seo geo ai аудит сайта",
                "page": "/seo-geo-ai-audit",
                "mentioned": True,
                "source_rank": 1,
                "answer_surface": "search-answer",
            },
            {
                "query": "видимость сайта в алисе ai",
                "page": "/alice-ai-visibility",
                "mentioned": True,
                "source_rank": 2,
                "answer_surface": "object-answer",
            },
            {
                "query": "как попасть в ответы алисы ai",
                "page": "/geo-faq",
                "mentioned": False,
                "source_rank": None,
                "answer_surface": "search-answer",
            },
        ],
        "competitors": [
            "example-competitor.ru",
            "another-market-site.ru",
            "media-source.ru",
        ],
        "opportunities": [
            "expand RU answer-ready sections for queries where the site ranks but is not cited",
            "strengthen expert and trust blocks on top money pages for Alice AI source selection",
            "compare cited competitor pages and turn missing patterns into content tasks",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
