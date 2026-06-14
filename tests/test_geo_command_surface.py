from __future__ import annotations

from tests.script_harness import run_script_main


def run_command(*args: str):
    return run_script_main("scripts/geo_command_surface.py", *args)


def test_help_works() -> None:
    result = run_command("--help")
    assert result.returncode == 0
    assert "command surface" in result.stdout.lower()


def test_catalog_works() -> None:
    result = run_command("catalog", "--format", "json")
    assert result.returncode == 0
    assert '"command": "audit"' in result.stdout
    assert '"command": "llmstxt"' in result.stdout
    assert '"command": "graph"' in result.stdout
    assert '"aliases": [' in result.stdout


def test_single_route_markdown() -> None:
    result = run_command("report")
    assert result.returncode == 0
    assert "# report" in result.stdout
    assert "client-delivery" in result.stdout
    assert "Outputs:" in result.stdout


def test_geo_prefixed_alias_works() -> None:
    result = run_command("/geo scan", "--format", "json")
    assert result.returncode == 0
    assert '"command": "audit"' in result.stdout
