from __future__ import annotations

import json
from pathlib import Path

from tests.script_harness import run_script_main


def test_capability_matrix_marks_live_and_starter_boundaries() -> None:
    result = run_script_main("scripts/capability_matrix.py", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    rows = {row["source_type"]: row for row in payload["rows"]}
    assert rows["gsc"]["delivery_state"] == "live_read_only_with_operator_credentials"
    assert rows["ga4"]["delivery_state"] == "starter_or_operator_guided"


def test_version_check_accepts_explicit_active_version() -> None:
    result = run_script_main(
        "scripts/version_consistency_check.py", "--expected", "6.11.1"
    )
    assert result.returncode == 0
    assert "version-consistency-ok:6.11.1" in result.stdout


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
