#!/usr/bin/env python3
"""Print a practical bootstrap plan for self-hosted deployment."""

from __future__ import annotations

import argparse
import json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print the bootstrap plan for demo, production-like, or scanner-oriented self-hosted deployment."
    )
    parser.add_argument(
        "--mode",
        choices=["demo", "production", "scanner"],
        default="demo",
        help="Bootstrap mode.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format.",
    )
    return parser


def build_plan(mode: str) -> dict:
    common_entrypoints = [
        "http://localhost:3000",
        "http://localhost:8000/docs",
    ]
    if mode == "production":
        return {
            "mode": mode,
            "commands": [
                "cp .env.production.example .env",
                "make install-backend",
                "make migrate",
                "docker compose up --build -d",
            ],
            "checks": [
                "Set strong APP_SECRET_KEY and database credentials.",
                "Put the stack behind HTTPS and a reverse proxy.",
                "Run make agent-self-check after first startup.",
            ],
            "entrypoints": common_entrypoints,
        }
    if mode == "scanner":
        return {
            "mode": mode,
            "commands": [
                "cp .env.production.example .env",
                "make install-backend",
                "make migrate",
                "docker compose up --build -d",
                "python scripts/agent_handoff_pack.py --task deploy-scanner --language en",
            ],
            "checks": [
                "Keep the scanner behind a consent-aware intake form or an authenticated operator flow.",
                "Verify HTTPS, reverse proxy headers, and report export behavior before opening access to third parties.",
                "Use make agent-self-check and make verify-demo as smoke checks after deployment.",
            ],
            "entrypoints": common_entrypoints,
            "delivery_surface": [
                "Frontend intake or operator dashboard on port 3000.",
                "Audit orchestration and reporting APIs on port 8000.",
                "Docs site validator or a custom intake page for low-friction URL submission.",
            ],
        }
    return {
        "mode": mode,
        "commands": [
            "cp .env.example .env",
            "make install-backend",
            "make turnkey-demo",
            "make verify-demo",
        ],
        "checks": [
            "Keep demo-safe defaults for the first local run.",
            "Sign in with demo@example.com / DemoPlatform123.",
            "Run make agent-self-check before claiming turnkey success.",
        ],
        "entrypoints": common_entrypoints,
    }


def main() -> int:
    args = build_parser().parse_args()
    plan = build_plan(args.mode)
    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    print(f"# Self-hosted bootstrap: {plan['mode']}")
    print("")
    print("## Commands")
    for command in plan["commands"]:
        print(f"- `{command}`")
    print("")
    print("## Checks")
    for item in plan["checks"]:
        print(f"- {item}")
    print("")
    print("## Entrypoints")
    for item in plan["entrypoints"]:
        print(f"- `{item}`")
    if "delivery_surface" in plan:
        print("")
        print("## Delivery surface")
        for item in plan["delivery_surface"]:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
