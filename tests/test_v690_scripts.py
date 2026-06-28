from __future__ import annotations

import json

from tests.script_harness import run_script_main


def test_integration_runtime_audit_returns_core_rows() -> None:
    result = run_script_main("scripts/integration_runtime_audit.py", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["source_count"] >= 6
    assert any(item["source_type"] == "gsc" for item in payload["rows"])


def test_serp_competitor_matrix_routes_commercial_keywords() -> None:
    result = run_script_main(
        "scripts/serp_competitor_matrix.py",
        "best seo agency",
        "what is geo",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["keyword_count"] == 2
    assert any(item["intent_lane"] == "commercial" for item in payload["rows"])


def test_link_gap_summary_reports_priority() -> None:
    result = run_script_main(
        "scripts/link_gap_summary.py",
        "--referring-domains",
        "40",
        "--lost-domains",
        "6",
        "--new-domains",
        "2",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["priority"] == "high"
    assert payload["authority_gap_score"] > 0


def test_benchmark_dataset_builder_includes_ru_layers() -> None:
    result = run_script_main(
        "scripts/benchmark_dataset_builder.py",
        "--market",
        "ru",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert "alice ai visibility" in payload["datasets"]
