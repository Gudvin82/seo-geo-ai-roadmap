#!/usr/bin/env python3
"""Render a machine-readable verification matrix for supported integrations and CMS flows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "app" / "backend"))

from app.services.cms import all_cms_contracts  # noqa: E402
from app.services.integrations import (  # noqa: E402
    all_integration_contracts,
    build_integration_verification_row,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the default integration verification matrix."
    )
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    rows = [
        build_integration_verification_row(
            contract["source_type"],
            label=contract["label"],
        )
        for contract in all_integration_contracts()
    ]
    rows.extend(
        {
            "id": f"cms-{contract['cms_type']}",
            "surface_type": "cms",
            "surface_name": contract["cms_type"].replace("_", " ").title(),
            "source_type": contract["cms_type"],
            "readiness_tier": contract["readiness_tier"],
            "proof_level": "contract_only",
            "credentials_status": "missing",
            "property_identifier": None,
            "ci_workflow": ".github/workflows/python-tests.yml",
            "ci_gates": [
                "inventory sync",
                "patch package generation",
                "approval-first apply path",
                "post-apply verification",
            ],
            "capabilities": [
                "inventory",
                "patch package",
                "reviewed writeback path",
            ],
            "production_flow": contract["production_path"],
            "verification_checks": [
                "credentials configured",
                "inventory synced",
                "approval path defined",
                "verify or rollback path available",
            ],
            "latest_snapshot_source": None,
            "latest_snapshot_summary": {},
            "next_step": contract["next_step"],
        }
        for contract in all_cms_contracts()
    )

    payload = {"schema_version": "v4.2.0", "rows": rows}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Integration verification matrix")
        for item in rows:
            print(
                f"- {item['surface_type']}::{item['source_type']} => {item['proof_level']} ({item['readiness_tier']})"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
