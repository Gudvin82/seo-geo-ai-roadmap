from __future__ import annotations

import json

from tests.script_harness import run_script_main


def test_checklist_generator_outputs_ru_focus_items() -> None:
    result = run_script_main(
        "scripts/checklist_generator.py",
        "--site-type",
        "local_business",
        "--market",
        "ru",
        "--focus",
        "local",
        "--focus",
        "geo",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["site_type"] == "local_business"
    titles = " ".join(item["title"] for item in payload["items"])
    assert "Yandex" in titles or "Alice AI" in titles


def test_semantic_gap_mapper_clusters_keywords() -> None:
    result = run_script_main(
        "scripts/semantic_gap_mapper.py",
        "--keyword",
        "seo audit price",
        "--keyword",
        "how to improve llms.txt",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["tracked_keywords"] == 2
    assert payload["clusters"]
    assert any(row["recommended_page_type"] for row in payload["clusters"])


def test_proof_pack_builder_returns_delta() -> None:
    result = run_script_main(
        "scripts/proof_pack_builder.py",
        "--site",
        "example.com",
        "--change",
        "expanded AI bot allow rules",
        "--before-score",
        "91",
        "--after-score",
        "94",
        "--fact",
        "robots.txt now allows 14/14 target bots",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["score_delta"] == 3.0
    assert payload["changes"]
