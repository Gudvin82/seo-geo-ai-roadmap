from __future__ import annotations

import json

from tests.script_harness import run_script_main


def test_community_showcase_builder_counts_public_and_synthetic_items() -> None:
    result = run_script_main(
        "scripts/community_showcase_builder.py",
        "docs/en/v430-case-anmalishev.md",
        "examples/synthetic-case-example-en.md",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["case_count"] == 2
    assert payload["public_case_count"] >= 1
    assert payload["synthetic_case_count"] >= 1


def test_launch_pack_generator_exposes_safe_claims_and_boundaries() -> None:
    result = run_script_main(
        "scripts/launch_pack_generator.py",
        "--version",
        "v6.8.5",
        "--format",
        "json",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["version"] == "v6.8.5"
    assert "free self-hosted SEO/GEO/AI platform" in payload["safe_public_claims"]
    assert "maintainer-operated hosted SaaS" in payload["do_not_claim"]
