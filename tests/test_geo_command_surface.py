from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "geo_command_surface.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_help_works() -> None:
    result = run_command("--help")
    assert result.returncode == 0
    assert "command surface" in result.stdout.lower()


def test_catalog_works() -> None:
    result = run_command("catalog", "--format", "json")
    assert result.returncode == 0
    assert '"command": "audit"' in result.stdout
    assert '"command": "llmstxt"' in result.stdout


def test_single_route_markdown() -> None:
    result = run_command("report")
    assert result.returncode == 0
    assert "# report" in result.stdout
    assert "client-delivery" in result.stdout
