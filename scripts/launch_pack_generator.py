from __future__ import annotations

import argparse
import json


def build_pack(version: str, repo_url: str) -> dict:
    return {
        "version": version,
        "repo_url": repo_url,
        "safe_public_claims": [
            "free self-hosted SEO/GEO/AI platform",
            "AI-agent-ready repository with app layer and working scripts",
            "foundation for your own audit or scanner service",
        ],
        "do_not_claim": [
            "maintainer-operated hosted SaaS",
            "guaranteed rankings or guaranteed AI citations",
            "fully autonomous changes without human review",
        ],
        "core_audiences": [
            "site owners",
            "SEO and GEO operators",
            "agencies building their own scanner service",
            "AI coding agents receiving a deployment or audit task",
        ],
        "launch_ctas": [
            "star the repository",
            "open a proof or case issue",
            "submit a content or tooling suggestion",
            "deploy a self-hosted demo and share findings",
        ],
        "proof_links": [
            "REAL_CASES.md",
            "SHOWCASE.md",
            "PUBLIC_PRODUCT_READINESS.md",
            "START_HERE_FOR_AI.md",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a safe public launch pack for the repository."
    )
    parser.add_argument("--version", default="v6.9.0", help="Release version label")
    parser.add_argument(
        "--repo-url",
        default="https://github.com/Gudvin82/seo-geo-ai-roadmap",
        help="Repository URL",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    args = parser.parse_args()

    payload = build_pack(args.version, args.repo_url)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"# Launch Pack {payload['version']}")
    print()
    print(f"- Repo: {payload['repo_url']}")
    print()
    print("## Safe public claims")
    print()
    for item in payload["safe_public_claims"]:
        print(f"- {item}")
    print()
    print("## Do not claim")
    print()
    for item in payload["do_not_claim"]:
        print(f"- {item}")
    print()
    print("## Core audiences")
    print()
    for item in payload["core_audiences"]:
        print(f"- {item}")
    print()
    print("## Launch CTAs")
    print()
    for item in payload["launch_ctas"]:
        print(f"- {item}")
    print()
    print("## Proof links")
    print()
    for item in payload["proof_links"]:
        print(f"- `{item}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
