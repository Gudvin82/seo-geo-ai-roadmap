from __future__ import annotations

from tests.script_harness import run_script_main


def run_command(*args: str):
    return run_script_main("scripts/agent_handoff_pack.py", *args)


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
