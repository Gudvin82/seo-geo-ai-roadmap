from __future__ import annotations

import argparse
import json


def build_pack(site_type: str, market: str) -> dict:
    return {
        "site_type": site_type,
        "market": market,
        "north_star": "turn audit findings into conversion-ready page, form, and CTA changes",
        "workstreams": [
            {
                "id": "landing_page_cro",
                "goal": "clarify who the offer is for, why it wins, and what action comes next",
                "inputs": ["audit report", "brand facts", "top money pages"],
                "outputs": ["hero rewrite", "proof block plan", "CTA hierarchy"],
                "owner": "growth_pm",
            },
            {
                "id": "form_and_lead_flow",
                "goal": "reduce friction in request, signup, and callback flows",
                "inputs": [
                    "form inventory",
                    "analytics events",
                    "heatmap or operator notes",
                ],
                "outputs": [
                    "field cleanup",
                    "objection handling",
                    "fallback contact path",
                ],
                "owner": "cro_operator",
            },
            {
                "id": "offer_and_pricing_clarity",
                "goal": "make commercial terms, scope, and proof obvious before the click",
                "inputs": ["service pages", "pricing notes", "sales objections"],
                "outputs": [
                    "offer matrix",
                    "pricing language pass",
                    "trust signals plan",
                ],
                "owner": "product_marketer",
            },
        ],
        "operator_rule": (
            "Do not ship CRO ideas as opinion only. Tie every change to a page, "
            "an objection, and a measurable next action."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a conversion-ops pack.")
    parser.add_argument("--site-type", default="service")
    parser.add_argument("--market", default="global")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    payload = build_pack(args.site_type, args.market)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Conversion Ops Pack")
    print()
    print(f"- site_type: `{payload['site_type']}`")
    print(f"- market: `{payload['market']}`")
    print(f"- north_star: {payload['north_star']}")
    print()
    print("## Workstreams")
    print()
    for item in payload["workstreams"]:
        print(f"### {item['id']}")
        print()
        print(f"- goal: {item['goal']}")
        print(f"- inputs: {', '.join(item['inputs'])}")
        print(f"- outputs: {', '.join(item['outputs'])}")
        print(f"- owner: {item['owner']}")
        print()
    print("## Operator Rule")
    print()
    print(payload["operator_rule"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
