from __future__ import annotations

import json
from pathlib import Path

from tests.script_harness import run_script_main


def test_capability_matrix_marks_live_and_starter_boundaries() -> None:
    result = run_script_main("scripts/capability_matrix.py", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    rows = {row["id"]: row for row in payload["rows"]}
    assert rows["integration:gsc"]["level"] == "foundation"
    assert rows["integration:ga4"]["level"] == "stub"
    assert rows["scanner"]["level"] == "production_ready"


def test_generated_capability_and_docs_parity_artifacts_are_current() -> None:
    capability = run_script_main(
        "scripts/capability_matrix.py",
        "--format",
        "json",
        "--output",
        "docs/generated/capability-matrix.json",
        "--check",
    )
    assert capability.returncode == 0, capability.stderr
    parity = run_script_main("scripts/docs_parity_check.py", "--check")
    assert parity.returncode == 0, parity.stderr


def test_version_check_accepts_explicit_active_version() -> None:
    result = run_script_main(
        "scripts/version_consistency_check.py", "--expected", "6.14.0"
    )
    assert result.returncode == 0
    assert "version-consistency-ok:6.14.0" in result.stdout


def test_scoring_calibration_marks_small_samples_as_insufficient(
    tmp_path: Path,
) -> None:
    dataset = tmp_path / "calibration.csv"
    dataset.write_text(
        "heuristic_score,observed_outcome\n60,12\n80,18\n", encoding="utf-8"
    )
    result = run_script_main("scripts/scoring_calibration.py", str(dataset))
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "insufficient_evidence"
