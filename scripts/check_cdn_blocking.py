#!/usr/bin/env python3
"""Check whether common AI bots appear blocked by CDN or edge rules."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._runtime_bootstrap import bootstrap_backend_imports  # noqa: E402

bootstrap_backend_imports()

from app.services.discoverability_checks import cdn_ai_blocking_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether CDN or WAF layers block public AI bots."
    )
    parser.add_argument("--url", required=True, help="Public page URL")
    args = parser.parse_args()

    report = cdn_ai_blocking_report(args.url)
    print(f"Status: {report['status'].upper()}")
    print(f"Detected CDN: {report['detected_cdn']}")
    print("Bot probes:")
    for item in report["probes"]:
        print(
            f"- {item['bot']}: status={item['status_code']} blocked={item['blocked']} final={item['final_url']}"
        )
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Limitation: {report['limitation']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
