from __future__ import annotations

import argparse
import json


DEFAULT_SOURCES = [
    "gsc",
    "ga4",
    "google_ads",
    "yandex_webmaster",
    "yandex_metrica",
    "yandex_direct",
]


def build_row(source: str) -> dict:
    recovery_mode = (
        "retry_then_operator_review"
        if source in {"gsc", "ga4", "yandex_webmaster", "yandex_metrica"}
        else "retry_then_manual_reconcile"
    )
    return {
        "source_type": source,
        "refresh_minutes": 1440 if "ads" not in source and "direct" not in source else 720,
        "token_rotation_days": 30 if "service" not in source else 45,
        "recovery_mode": recovery_mode,
        "proof_status": "operator_ready_runtime",
        "next_step": f"validate {source} credentials and save the first reviewed runtime snapshot",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a managed-runtime audit matrix for core integrations."
    )
    parser.add_argument(
        "--sources", nargs="*", default=DEFAULT_SOURCES, help="Sources to include"
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    rows = [build_row(source) for source in args.sources]
    payload = {
        "source_count": len(rows),
        "rows": rows,
        "operator_rule": (
            "Treat credential lifecycle, refresh cadence, retry policy, and proof "
            "status as one managed-runtime operating surface."
        ),
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("# Integration Runtime Audit\n")
    for row in rows:
        print(f"## {row['source_type']}\n")
        print(f"- Refresh minutes: {row['refresh_minutes']}")
        print(f"- Token rotation days: {row['token_rotation_days']}")
        print(f"- Recovery mode: {row['recovery_mode']}")
        print(f"- Proof status: {row['proof_status']}")
        print(f"- Next step: {row['next_step']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
