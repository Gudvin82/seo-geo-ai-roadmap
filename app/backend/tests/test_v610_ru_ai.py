from __future__ import annotations

from app.services.scoring import benchmark_status, ru_geo_score


def test_ru_geo_score_rewards_alice_and_yandex_stack() -> None:
    integration_metrics = {
        "yandex_webmaster": {"metrics": {}, "rows": []},
        "yandex_metrica": {"metrics": {}, "rows": []},
        "yandex_direct": {"metrics": {}, "rows": []},
        "yandex_business": {"metrics": {"review_count": 18}, "rows": []},
        "yandex_neuro": {
            "metrics": {
                "yandex_additional_access": 1,
                "ru_answer_ready_pages": 9,
                "trust_blocks_present": 1,
                "legal_blocks_present": 1,
            },
            "rows": [],
        },
        "alice_ai_visibility": {
            "metrics": {
                "share_of_voice": 0.14,
                "weekly_delta": 0.03,
                "query_coverage": 0.62,
                "queries_with_own_mentions": 8,
                "insufficient_data": False,
            },
            "rows": [],
        },
    }
    score, components = ru_geo_score(integration_metrics=integration_metrics)
    assert score >= 70
    assert components["alice_ai_visibility"] > 0
    assert components["yandex_neuro"] > 0
    assert benchmark_status("ru_geo_score", score) in {
        "better_than_baseline",
        "worse_than_baseline",
    }


def test_ru_geo_score_handles_insufficient_alice_data() -> None:
    score, components = ru_geo_score(
        integration_metrics={
            "alice_ai_visibility": {
                "metrics": {
                    "share_of_voice": 0.0,
                    "query_coverage": 0.0,
                    "queries_with_own_mentions": 0,
                    "insufficient_data": True,
                },
                "rows": [],
            }
        }
    )
    assert score == components["alice_ai_visibility"]
    assert components["alice_ai_visibility"] == 3.0
