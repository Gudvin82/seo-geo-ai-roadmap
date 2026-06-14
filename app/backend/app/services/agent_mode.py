from __future__ import annotations

import json
from typing import Any

from ..models import AuditRun, NotificationEndpoint, Project, ScanJob, ScheduledCheck
from .task_center import (
    build_task_bundle_from_audit_run,
    build_task_bundle_from_scan_job,
)

AGENT_MODE_CONTRACT_VERSION = "v4.6.0"
SUPPORTED_AGENT_MODES = [
    "manual",
    "scheduled",
    "watch",
    "agent-review",
    "agent-plan",
    "agent-fix-proposal",
]
SAFE_BOUNDARIES = [
    "Agent mode can analyze, summarize, compare, alert, and build fix packs.",
    "Agent mode must not publish production changes without explicit approval.",
    "Agent mode may prepare PR-ready payloads, CMS draft payloads, or issue exports.",
]


def agent_mode_contract() -> dict[str, Any]:
    return {
        "contract_version": AGENT_MODE_CONTRACT_VERSION,
        "supported_modes": SUPPORTED_AGENT_MODES,
        "safe_boundaries": SAFE_BOUNDARIES,
        "deliverables": [
            "executive summary",
            "recommendation set",
            "task bundle",
            "fix proposal contract",
            "notification payload",
        ],
        "notification_channels": ["webhook", "email", "telegram"],
    }


def agent_mode_overview(
    *,
    project: Project,
    latest_audit: AuditRun | None,
    latest_scan: ScanJob | None,
    scheduled_checks: list[ScheduledCheck],
    notification_endpoints: list[NotificationEndpoint],
) -> dict[str, Any]:
    latest_sources = {
        "latest_audit_run_id": latest_audit.id if latest_audit else None,
        "latest_scan_job_id": latest_scan.id if latest_scan else None,
        "latest_audit_status": latest_audit.status if latest_audit else "not-run",
        "latest_scan_status": latest_scan.status if latest_scan else "not-run",
    }
    return {
        "contract_version": AGENT_MODE_CONTRACT_VERSION,
        "project_id": project.id,
        "latest_sources": latest_sources,
        "supported_modes": SUPPORTED_AGENT_MODES,
        "scheduler_status": {
            "scheduled_checks": len(scheduled_checks),
            "active_checks": sum(1 for item in scheduled_checks if item.is_enabled),
            "durable_queue_status": "db-backed-recoverable-scan-worker",
            "retry_policy": "scheduler + recoverable scan queue + notification retries",
        },
        "alert_policy": [
            "Trigger alerts on failed scans, degraded executive score, or missing sync freshness.",
            "Send lighter summaries for watch mode and denser packs for agent-plan or fix-proposal modes.",
        ],
        "notification_channels": [item.channel_type for item in notification_endpoints],
        "safe_action_boundary": SAFE_BOUNDARIES,
        "next_recommended_actions": _next_actions(
            latest_audit, latest_scan, scheduled_checks
        ),
    }


def build_agent_mode_run(
    *,
    project: Project,
    mode: str,
    source_type: str,
    source_id: int | None,
    benchmark: str | None,
    audit_run: AuditRun | None,
    scan_job: ScanJob | None,
) -> dict[str, Any]:
    tasks_bundle: dict[str, Any]
    summary: str
    recommendations: list[str]
    alerts: list[str]

    if source_type == "scan_job" and scan_job is not None:
        machine_report = _machine_report(scan_job)
        tasks_bundle = build_task_bundle_from_scan_job(scan_job, machine_report)
        summary = machine_report.get("executive_summary", "Scanner review completed.")
        recommendations = [
            item["recommended_fix"] for item in tasks_bundle["tasks"][:5]
        ]
        alerts = _scan_alerts(scan_job, machine_report)
        resolved_source_id = scan_job.id
    elif audit_run is not None:
        findings = json.loads(audit_run.finding_groups_json or "[]")
        tasks_bundle = build_task_bundle_from_audit_run(audit_run, findings)
        summary = f"Audit run {audit_run.id} is ready for {mode} with {len(findings)} finding(s)."
        recommendations = [
            item["recommended_fix"] for item in tasks_bundle["tasks"][:5]
        ]
        alerts = _audit_alerts(audit_run, findings)
        resolved_source_id = audit_run.id
    else:
        tasks_bundle = {
            "tasks": [],
        }
        summary = "No source was available for agent mode."
        recommendations = []
        alerts = ["Run a scan or audit before starting agent mode."]
        resolved_source_id = source_id or 0

    if benchmark:
        recommendations.insert(
            0, f"Compare the current source against benchmark profile `{benchmark}`."
        )

    return {
        "contract_version": AGENT_MODE_CONTRACT_VERSION,
        "mode": mode,
        "project_id": project.id,
        "source_type": source_type,
        "source_id": str(resolved_source_id),
        "benchmark": benchmark,
        "summary": summary,
        "recommendations": recommendations,
        "alerts": alerts,
        "follow_up_tasks": tasks_bundle.get("tasks", [])[:8],
        "safe_actions": [
            "create issues",
            "generate fix pack",
            "prepare PR proposal",
            "prepare CMS draft payload",
        ],
        "approval_required_for": [
            "publish CMS changes",
            "merge code changes",
            "run active production writeback",
        ],
    }


def _machine_report(scan_job: ScanJob) -> dict[str, Any]:
    for artifact in json.loads(scan_job.report_artifacts_json or "[]"):
        if artifact.get("kind") == "machine_report":
            try:
                with open(artifact["path"], "r", encoding="utf-8") as handle:
                    return json.load(handle)
            except FileNotFoundError:
                break
    return {
        "executive_summary": "Scanner report is not available yet.",
        "issues": [],
        "target_domain": scan_job.target_domain,
        "target_url": scan_job.normalized_url,
        "scan_mode": scan_job.scan_mode,
    }


def _scan_alerts(scan_job: ScanJob, summary: dict[str, Any]) -> list[str]:
    alerts = []
    if scan_job.status in {"failed", "partial_success"}:
        alerts.append(f"Scan job {scan_job.id} ended in {scan_job.status}.")
    if len(summary.get("issues", [])) >= 4:
        alerts.append("Issue volume is high enough to justify an executive re-check.")
    return alerts


def _audit_alerts(audit_run: AuditRun, findings: list[dict[str, Any]]) -> list[str]:
    alerts = []
    if (audit_run.summary_score or 0) < 60:
        alerts.append("Executive score is below the healthy threshold.")
    if any(float(item.get("priority_score", 0) or 0) >= 80 for item in findings):
        alerts.append("One or more findings are at critical priority.")
    return alerts


def _next_actions(
    latest_audit: AuditRun | None,
    latest_scan: ScanJob | None,
    scheduled_checks: list[ScheduledCheck],
) -> list[str]:
    actions = []
    if latest_scan is None:
        actions.append("Start with a passive URL audit through the scanner intake.")
    if latest_audit is None:
        actions.append(
            "Run the first structured audit to unlock executive and task layers."
        )
    if not scheduled_checks:
        actions.append(
            "Create at least one scheduled check so agent mode has a monitoring cadence."
        )
    actions.append("Connect at least one notification channel for watch-mode alerts.")
    return actions
