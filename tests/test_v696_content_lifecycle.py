from __future__ import annotations

import json
from pathlib import Path

from tests.script_harness import run_script_main


def test_content_lifecycle_runs_end_to_end(tmp_path: Path) -> None:
    result = run_script_main(
        "scripts/content_lifecycle.py",
        "--manifest",
        "examples/content-lifecycle/manifest.json",
        "--output-dir",
        str(tmp_path),
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "v6.9.6"
    assert {"gsc", "yandex_webmaster", "wordstat"}.issubset(
        {source for item in payload["demand"] for source in item["sources"]}
    )
    assert payload["cannibalization_conflicts"]
    assert payload["draft_checks"][0]["status"] == "ready_for_human_approval"
    assert payload["monitoring"]["opportunities_4_15"]
    assert payload["advisor"]["mode"] == "deterministic_advisor_no_writeback"
    assert (tmp_path / "content-lifecycle-report.json").exists()
    assert (tmp_path / "cover.svg").exists()


def test_weak_draft_is_blocked() -> None:
    import importlib.util

    path = Path(__file__).parents[1] / "scripts" / "content_lifecycle.py"
    spec = importlib.util.spec_from_file_location("content_lifecycle_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.validate_draft({"title": "Thin", "slug": "Bad Slug"})
    assert result["status"] == "blocked"
    assert result["failure_count"] >= 5


def test_indexnow_dry_run_does_not_claim_indexing() -> None:
    result = run_script_main(
        "scripts/indexnow_submit.py",
        "--host",
        "example.com",
        "--key",
        "12345678",
        "--url",
        "https://example.com/new-page",
        "--dry-run",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["submission"]["status"] == "not_sent"
    assert "do not guarantee indexing" in payload["boundary"]


def test_indexnow_rejects_cross_host_url() -> None:
    result = run_script_main(
        "scripts/indexnow_submit.py",
        "--host",
        "example.com",
        "--key",
        "12345678",
        "--url",
        "https://other.example/new-page",
        "--dry-run",
    )
    assert result.returncode != 0
    assert "match --host" in result.stderr
