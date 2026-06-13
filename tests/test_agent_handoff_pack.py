from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "agent_handoff_pack.py"


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
    assert "handoff prompt" in result.stdout.lower()


def test_audit_site_markdown_includes_target_url() -> None:
    result = run_command(
        "--task",
        "audit-site",
        "--language",
        "en",
        "--target-url",
        "https://example.com",
    )
    assert result.returncode == 0
    assert "Target URL: https://example.com" in result.stdout
    assert "executive summary" in result.stdout


def test_deploy_scanner_json_mentions_architecture_note() -> None:
    result = run_command(
        "--task",
        "deploy-scanner",
        "--language",
        "ru",
        "--format",
        "json",
    )
    assert result.returncode == 0
    assert '"task": "deploy-scanner"' in result.stdout
    assert "ARCHITECTURE_NOTE_RU.md" in result.stdout
