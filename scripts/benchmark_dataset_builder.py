from __future__ import annotations

import argparse
import json


def build_dataset(market: str) -> dict:
    datasets = [
        "query cluster coverage",
        "content gap count",
        "referring domain growth",
        "top-10 share",
        "landing-page conversion delta",
    ]
    if market == "ru":
        datasets.extend(
            [
                "yandex regional visibility",
                "alice ai visibility",
                "ru local trust and review density",
            ]
        )
    return {
        "market": market,
        "datasets": datasets,
        "operator_rule": (
            "Benchmark SEO with demand, authority, and conversion data; treat GEO/AI "
            "as an additional layer, not the only score."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a benchmark dataset pack for classic SEO operations."
    )
    parser.add_argument("--market", default="global", choices=("global", "ru"))
    parser.add_argument("--format", default="json", choices=("json", "markdown"))
    args = parser.parse_args()
    payload = build_dataset(args.market)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Benchmark Dataset Builder\n")
    print(f"- Market: {payload['market']}\n")
    for item in payload["datasets"]:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
