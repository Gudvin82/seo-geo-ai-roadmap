from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ScheduleDescriptor:
    schedule_mode: str
    execution_path: str
    next_run_hint: str
    last_status: str
    limitations: list[str]


def describe_schedule(
    frequency: str,
    check_type: str,
    is_enabled: bool,
    config: dict,
    last_run_at: datetime | None,
) -> ScheduleDescriptor:
    schedule_mode = str(config.get("schedule_mode", "cron")).strip().lower() or "cron"
    execution_path = {
        "app": "app worker or background runner",
        "github_actions": "scheduled GitHub Action",
        "cron": "cron-compatible CLI runner",
    }.get(schedule_mode, "cron-compatible CLI runner")
    next_run_hint = _next_run_hint(frequency, last_run_at)
    last_status = str(config.get("last_status", "queued" if is_enabled else "disabled"))
    limitations = [
        "Local or self-hosted operators must configure their own scheduler host.",
        "Scheduled runs do not remove the need for human review of volatile AI outputs.",
    ]
    if check_type in {"ai_sov", "audit"}:
        limitations.append(
            "Provider quotas, prompt volatility, and external network conditions can affect repeatability."
        )
    return ScheduleDescriptor(
        schedule_mode=schedule_mode,
        execution_path=execution_path,
        next_run_hint=next_run_hint,
        last_status=last_status,
        limitations=limitations,
    )


def _next_run_hint(frequency: str, last_run_at: datetime | None) -> str:
    normalized = frequency.strip().lower()
    base_time = last_run_at or datetime.utcnow()
    if normalized == "daily":
        return (base_time + timedelta(days=1)).isoformat() + "Z"
    if normalized == "weekly":
        return (base_time + timedelta(days=7)).isoformat() + "Z"
    if normalized == "monthly":
        return (base_time + timedelta(days=30)).isoformat() + "Z"
    return f"Follow custom schedule expression for '{frequency}'."
