from __future__ import annotations

import argparse
import json


def build_pack(channel: str, version: str) -> dict:
    return {
        "channel": channel,
        "version": version,
        "assets": [
            "safe claim block",
            "one-paragraph summary",
            "feature bullets",
            "proof links",
            "feedback CTA",
        ],
        "operator_checks": [
            "claim matches PUBLIC_PRODUCT_READINESS.md",
            "latest release links are correct",
            "proof links point to public bounded evidence",
            "out-of-scope surfaces are not overstated",
        ],
        "operator_rule": (
            "Launch materials should compress the product honestly without hiding the self-hosted boundary."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a launch-ops pack.")
    parser.add_argument("--channel", default="social-post")
    parser.add_argument("--version", default="v6.9.6")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    payload = build_pack(args.channel, args.version)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Launch Ops Pack")
    print()
    print(f"- channel: `{payload['channel']}`")
    print(f"- version: `{payload['version']}`")
    print()
    print("## Assets")
    print()
    for item in payload["assets"]:
        print(f"- {item}")
    print()
    print("## Operator Checks")
    print()
    for item in payload["operator_checks"]:
        print(f"- {item}")
    print()
    print("## Operator Rule")
    print()
    print(payload["operator_rule"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
