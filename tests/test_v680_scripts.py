from __future__ import annotations

import json

from tests.script_harness import run_script_main


def test_case_library_builder_indexes_cases() -> None:
    result = run_script_main(
        "scripts/case_library_builder.py",
        "docs/en/v430-case-anmalishev.md",
        "examples/synthetic-case-example-en.md",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["case_count"] == 2
    assert any(item["case_type"] == "synthetic" for item in payload["cases"])


def test_synthetic_case_builder_marks_case_as_synthetic() -> None:
    result = run_script_main(
        "scripts/synthetic_case_builder.py",
        "--name",
        "Synthetic Demo",
        "--before-score",
        "70",
        "--after-score",
        "82",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["case_kind"] == "synthetic_example"
    assert payload["score_delta"] == 12.0


def test_issue_pack_generator_creates_rows() -> None:
    result = run_script_main(
        "scripts/issue_pack_generator.py",
        "--project",
        "example.com",
        "--finding",
        "Thin proof|high|content_lead|add stronger case proof",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["priority"] == "high"
