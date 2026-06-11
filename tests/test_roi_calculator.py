from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "roi_calculator.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_happy_path_calculation() -> None:
    result = run_command(
        "--traffic",
        "5000",
        "--conversion-rate",
        "0.03",
        "--lead-to-sale-rate",
        "0.2",
        "--average-check",
        "1200",
        "--margin-rate",
        "0.45",
        "--seo-cost",
        "1500",
        "--ai-referred-share",
        "0.1",
    )
    assert result.returncode == 0
    assert "Visits: 5000.00" in result.stdout
    assert "Leads: 150.00" in result.stdout
    assert "Estimated ROI / ROMI: 980.00%" in result.stdout


def test_zero_traffic_edge_case() -> None:
    result = run_command(
        "--traffic",
        "0",
        "--conversion-rate",
        "0.03",
        "--lead-to-sale-rate",
        "0.2",
        "--average-check",
        "1200",
        "--margin-rate",
        "0.45",
        "--seo-cost",
        "1500",
    )
    assert result.returncode == 0
    assert "Visits: 0.00" in result.stdout
    assert "Revenue: 0.00" in result.stdout


def test_invalid_numeric_input_handling() -> None:
    result = run_command(
        "--traffic",
        "1000",
        "--conversion-rate",
        "1.5",
        "--lead-to-sale-rate",
        "0.2",
        "--average-check",
        "1200",
        "--margin-rate",
        "0.45",
        "--seo-cost",
        "1500",
    )
    assert result.returncode == 1
    assert "must be between 0 and 1" in result.stderr
