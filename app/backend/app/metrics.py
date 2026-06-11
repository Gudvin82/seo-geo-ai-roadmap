from __future__ import annotations

from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

AUTH_REQUESTS = Counter(
    "discoverability_auth_requests_total",
    "Authentication requests",
    ["endpoint", "status"],
)
AUDIT_RUNS = Counter(
    "discoverability_audit_runs_total",
    "Audit runs created",
    ["status"],
)
PROVIDER_CALLS = Counter(
    "discoverability_provider_calls_total",
    "Provider calls",
    ["provider", "status"],
)
PROVIDER_FAILURES = Counter(
    "discoverability_provider_failures_total",
    "Provider failures",
    ["provider"],
)
REPORT_GENERATIONS = Counter(
    "discoverability_report_generations_total",
    "Reports generated",
    ["language"],
)
INVITE_ACCEPTANCES = Counter(
    "discoverability_invite_acceptances_total",
    "Workspace invite acceptances",
    ["role"],
)
ROLE_CHANGES = Counter(
    "discoverability_role_changes_total",
    "Workspace role changes",
    ["role"],
)
SOV_RUNS = Counter(
    "discoverability_sov_runs_total",
    "AI Share of Voice runs",
    ["status"],
)
NOTIFICATION_DELIVERIES = Counter(
    "discoverability_notification_deliveries_total",
    "Notification delivery attempts",
    ["channel", "status"],
)


def metrics_payload() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
