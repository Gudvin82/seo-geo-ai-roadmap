from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize basic link-gap priorities from referring-domain counts."
    )
    parser.add_argument("--referring-domains", type=int, required=True)
    parser.add_argument("--lost-domains", type=int, default=0)
    parser.add_argument("--new-domains", type=int, default=0)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    authority_gap = max(0, 100 - args.referring_domains)
    payload = {
        "referring_domains": args.referring_domains,
        "lost_domains": args.lost_domains,
        "new_domains": args.new_domains,
        "authority_gap_score": round(authority_gap / 100, 2),
        "priority": "high" if args.lost_domains > args.new_domains else "watch",
        "recommended_actions": [
            "recover lost high-trust domains first",
            "turn proof packs into outreach and editorial assets",
            "separate local citations from authority links in reporting",
        ],
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Link Gap Summary\n")
    for key, value in payload.items():
        if key == "recommended_actions":
            continue
        print(f"- {key}: {value}")
    print("\n## Recommended actions\n")
    for item in payload["recommended_actions"]:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
