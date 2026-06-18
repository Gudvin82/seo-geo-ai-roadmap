#!/usr/bin/env python3
"""Evaluate whether HTML is segmented cleanly for downstream RAG chunking."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._runtime_bootstrap import bootstrap_backend_imports  # noqa: E402

bootstrap_backend_imports()

from app.services.discoverability_checks import (  # noqa: E402
    fetch_url_text,
    rag_chunk_readiness_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check RAG chunk readiness.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public page URL")
    group.add_argument("--file", help="Local HTML file path")
    args = parser.parse_args()

    html = (
        fetch_url_text(args.url)
        if args.url
        else Path(args.file).read_text(encoding="utf-8")
    )
    report = rag_chunk_readiness_report(html)
    print(f"Status: {report['status'].upper()}")
    print(f"Heading count: {report['heading_count']}")
    print(f"Text blocks: {report['text_block_count']}")
    print(f"Average block length: {report['average_block_length']}")
    print(f"Long blocks: {report['long_block_count']}")
    print(f"Definition signals: {report['definition_signal_count']}")
    if report["warnings"]:
        print("Warnings:")
        for item in report["warnings"]:
            print(f"- {item}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Limitation: {report['limitation']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
