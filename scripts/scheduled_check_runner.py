#!/usr/bin/env python3
"""Show how scheduled checks can be executed in cron or GitHub Actions."""

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a schedule execution plan for recurring audits, AI SoV, and validation checks."
    )
    parser.add_argument("--project-id", type=int, required=True, help="Project ID")
    parser.add_argument(
        "--check-type",
        required=True,
        choices=["audit", "ai_sov", "llms", "robots", "schema"],
        help="Type of recurring check to plan",
    )
    parser.add_argument(
        "--frequency",
        default="weekly",
        choices=["daily", "weekly", "monthly", "custom"],
        help="Schedule frequency",
    )
    parser.add_argument(
        "--schedule-mode",
        default="cron",
        choices=["cron", "github_actions", "app"],
        help="Execution mode",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = {
        "project_id": args.project_id,
        "check_type": args.check_type,
        "frequency": args.frequency,
        "schedule_mode": args.schedule_mode,
        "recommended_artifacts": [
            "run receipt",
            "audit log event",
            "report or validation summary",
        ],
        "limitations": [
            "External provider volatility still requires human review.",
            "Local scheduling needs cron, worker, or GitHub Actions wiring.",
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
