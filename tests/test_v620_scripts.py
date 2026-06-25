from __future__ import annotations

import json

from tests.script_harness import run_script_main


def run(script_name: str):
    return run_script_main(f"scripts/{script_name}")


def test_keyword_research_stub_returns_rows() -> None:
    result = run("keyword_research_stub.py")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["metrics"]["tracked_keywords"] > 0
    assert payload["rows"]


def test_competitor_intelligence_stub_returns_gaps() -> None:
    result = run("competitor_intelligence_stub.py")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["metrics"]["tracked_competitors"] > 0
    assert payload["opportunities"]


def test_backlink_intelligence_stub_returns_domains() -> None:
    result = run("backlink_intelligence_stub.py")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["metrics"]["referring_domains"] > 0
    assert payload["rows"]


def test_rank_tracking_stub_returns_queries() -> None:
    result = run("rank_tracking_stub.py")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["metrics"]["tracked_queries"] > 0
    assert payload["rows"]


def test_version_consistency_script_passes() -> None:
    result = run_script_main("scripts/version_consistency_check.py")
    assert result.returncode == 0
    assert "version-consistency-ok" in result.stdout
