from __future__ import annotations

from tests.script_harness import run_script_main


def run_command(*args: str):
    return run_script_main("scripts/bootstrap_self_hosted.py", *args)


def test_help_works() -> None:
    result = run_command("--help")
    assert result.returncode == 0
    assert "bootstrap plan" in result.stdout.lower()


def test_demo_markdown_output() -> None:
    result = run_command("--mode", "demo")
    assert result.returncode == 0
    assert "make turnkey-demo" in result.stdout
    assert "demo@example.com" in result.stdout


def test_production_json_output() -> None:
    result = run_command("--mode", "production", "--format", "json")
    assert result.returncode == 0
    assert '"mode": "production"' in result.stdout
    assert "APP_SECRET_KEY" in result.stdout


def test_scanner_markdown_output() -> None:
    result = run_command("--mode", "scanner")
    assert result.returncode == 0
    assert "deploy a reusable scanner" not in result.stdout.lower()
    assert "Delivery surface" in result.stdout
    assert "agent_handoff_pack.py --task deploy-scanner" in result.stdout
