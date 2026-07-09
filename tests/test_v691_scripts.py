from __future__ import annotations

import json

from tests.script_harness import run_script_main


def test_conversion_ops_pack_exposes_workstreams() -> None:
    result = run_script_main(
        "scripts/conversion_ops_pack.py",
        "--site-type",
        "saas",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["site_type"] == "saas"
    assert len(payload["workstreams"]) >= 3


def test_content_growth_ops_exposes_architecture_pillars() -> None:
    result = run_script_main(
        "scripts/content_growth_ops.py",
        "--vertical",
        "legal",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["vertical"] == "legal"
    assert any(item["id"] == "site_architecture" for item in payload["pillars"])


def test_customer_research_pack_exposes_direct_language_tracks() -> None:
    result = run_script_main(
        "scripts/customer_research_pack.py",
        "--audience",
        "founders",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["audience"] == "founders"
    assert any(item["id"] == "voice_of_customer" for item in payload["research_tracks"])


def test_launch_ops_pack_tracks_release_version() -> None:
    result = run_script_main(
        "scripts/launch_ops_pack.py",
        "--version",
        "v6.9.1",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["version"] == "v6.9.1"
    assert any("proof" in item.lower() for item in payload["assets"])
