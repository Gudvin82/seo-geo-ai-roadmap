from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/geo_intelligence.py"), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_audit_emits_evidence_contract() -> None:
    result = run(
        "audit",
        "https://example.com",
        "--input",
        str(ROOT / "examples/geo-intelligence-observations.json"),
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["contract_version"] == "v1"
    assert payload["findings"][0]["evidence"][0]["evidence_type"] == "verified"
    assert payload["scorecard"]["score"] is not None
    assert payload["roadmap"]


def test_doctor_is_machine_readable() -> None:
    result = run("doctor")
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "ready"


def test_analyzer_runner_is_not_an_alias_for_audit() -> None:
    result = run(
        "entity",
        "https://example.com",
        "--input",
        str(ROOT / "examples/geo-intelligence-observations.json"),
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["analyzer"] == "entity"
    assert payload["status"] == "scored"


def test_citation_runner_consumes_citation_evidence() -> None:
    result = run(
        "citation",
        "https://example.com",
        "--input",
        str(ROOT / "examples/geo-intelligence-observations.json"),
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "scored"
