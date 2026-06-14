from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime
from typing import Any

from ..models import AuditRun, ScanJob

TASK_CONTRACT_VERSION = "v5.1.0"


def build_task_bundle_from_scan_job(
    scan_job: ScanJob, summary: dict[str, Any]
) -> dict[str, Any]:
    tasks = []
    for index, issue in enumerate(summary.get("issues", []), start=1):
        tasks.append(
            {
                "id": f"scan-{scan_job.id}-task-{index}",
                "issue_type": issue.get("issue_id", "scanner_issue"),
                "severity": issue.get("severity", "medium"),
                "affected_surface": _surface_from_issue(issue),
                "affected_pages": [summary.get("target_url", scan_job.normalized_url)],
                "recommended_fix": issue.get(
                    "recommended_action", "Review the finding and prepare a fix pack."
                ),
                "workflow": _workflow_from_issue(issue),
                "suggested_owner": _owner_from_issue(issue),
                "evidence": [
                    issue.get("title", "Issue"),
                    issue.get("recommended_action", ""),
                ],
                "estimated_impact": _impact_from_severity(
                    issue.get("severity", "medium")
                ),
                "status": "open",
                "source_ref": f"scan_job:{scan_job.id}",
            }
        )
    return _bundle(
        source_type="scan_job",
        source_id=str(scan_job.id),
        summary_text=summary.get(
            "executive_summary", "Scanner results require review."
        ),
        target_label=summary.get("target_domain", scan_job.target_domain),
        tasks=tasks,
    )


def build_task_bundle_from_audit_run(
    audit_run: AuditRun, findings: list[dict[str, Any]]
) -> dict[str, Any]:
    tasks = []
    for index, finding in enumerate(findings, start=1):
        tasks.append(
            {
                "id": f"audit-{audit_run.id}-task-{index}",
                "issue_type": finding.get("slug", finding.get("title", "audit_finding"))
                .lower()
                .replace(" ", "_"),
                "severity": _severity_from_priority(finding),
                "affected_surface": finding.get("surface", "discoverability"),
                "affected_pages": [
                    finding.get("page")
                    or finding.get("url")
                    or audit_run.target_url
                    or ""
                ],
                "recommended_fix": finding.get(
                    "recommendation", "Turn this finding into a fix brief."
                ),
                "workflow": finding.get(
                    "workflow", "review -> patch pack -> re-measure"
                ),
                "suggested_owner": finding.get("owner", _owner_from_finding(finding)),
                "evidence": [finding.get("summary", ""), finding.get("notes", "")],
                "estimated_impact": finding.get("benchmark_status", "meaningful"),
                "status": "open",
                "source_ref": f"audit_run:{audit_run.id}",
            }
        )
    return _bundle(
        source_type="audit_run",
        source_id=str(audit_run.id),
        summary_text=f"Audit run {audit_run.id} generated {len(tasks)} prioritized tasks.",
        target_label=audit_run.target_url or f"project-{audit_run.project_id}",
        tasks=tasks,
    )


def export_bundle(
    bundle: dict[str, Any],
    target: str,
    *,
    repository: str | None = None,
    token_env_var: str | None = None,
    dry_run: bool = True,
) -> dict[str, Any]:
    if target == "github_issues":
        return _export_github(
            bundle, repository=repository, token_env_var=token_env_var, dry_run=dry_run
        )
    return {
        "target": target,
        "mode": "template",
        "exported_count": len(bundle.get("tasks", [])),
        "created_items": [],
        "payload_preview": {
            "tasks": bundle.get("tasks", []),
            "notes": f"{target} adapter is scaffolded as a payload template in v4.0.0.",
        },
        "next_step": f"Connect a real {target} token and map the payload fields into your workspace automation.",
    }


def _bundle(
    *,
    source_type: str,
    source_id: str,
    summary_text: str,
    target_label: str,
    tasks: list[dict[str, Any]],
) -> dict[str, Any]:
    markdown_lines = [f"# Task bundle for {target_label}", ""]
    client_lines = [summary_text, "", "Recommended work queue:"]
    for task in tasks:
        markdown_lines.extend(
            [
                f"- [{task['severity']}] {task['recommended_fix']}",
                f"  Surface: {task['affected_surface']}",
                f"  Workflow: {task['workflow']}",
            ]
        )
        client_lines.append(f"- {task['recommended_fix']} ({task['estimated_impact']})")
    return {
        "contract_version": TASK_CONTRACT_VERSION,
        "source_type": source_type,
        "source_id": source_id,
        "generated_at": datetime.utcnow(),
        "summary": summary_text,
        "tasks": tasks,
        "markdown_ready": "\n".join(markdown_lines) + "\n",
        "client_ready_summary": "\n".join(client_lines) + "\n",
    }


def _export_github(
    bundle: dict[str, Any],
    *,
    repository: str | None,
    token_env_var: str | None,
    dry_run: bool,
) -> dict[str, Any]:
    issues = []
    for task in bundle.get("tasks", []):
        issues.append(
            {
                "title": f"[{task['severity'].upper()}] {task['recommended_fix'][:72]}",
                "body": (
                    f"Source: `{task['source_ref']}`\n\n"
                    f"Surface: `{task['affected_surface']}`\n"
                    f"Owner: `{task['suggested_owner']}`\n"
                    f"Workflow: `{task['workflow']}`\n"
                    f"Impact: `{task['estimated_impact']}`\n\n"
                    "Evidence:\n"
                    + "\n".join(
                        f"- {item}" for item in task.get("evidence", []) if item
                    )
                ),
                "labels": [
                    "discoverability",
                    task["severity"],
                    task["affected_surface"].replace(" ", "-"),
                ],
            }
        )
    if dry_run or not repository or not token_env_var or not os.getenv(token_env_var):
        return {
            "target": "github_issues",
            "mode": "preview",
            "exported_count": len(issues),
            "created_items": [],
            "payload_preview": {"repository": repository, "issues": issues},
            "next_step": "Set repository + token env var and rerun with dry_run=false to create real GitHub issues.",
        }

    created_items = []
    token = os.getenv(token_env_var, "")
    for issue in issues:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repository}/issues",
            data=json.dumps(issue).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(
            request, timeout=20
        ) as response:  # pragma: no cover - networked path
            payload = json.loads(response.read().decode("utf-8"))
            created_items.append(
                {
                    "id": payload.get("id"),
                    "number": payload.get("number"),
                    "url": payload.get("html_url"),
                }
            )
    return {
        "target": "github_issues",
        "mode": "live",
        "exported_count": len(created_items),
        "created_items": created_items,
        "payload_preview": {"repository": repository},
        "next_step": "Review the created issues, assign owners, and feed them back into patch and re-measurement flows.",
    }


def _surface_from_issue(issue: dict[str, Any]) -> str:
    issue_id = str(issue.get("issue_id", ""))
    if "schema" in issue_id:
        return "structured-data"
    if "bot" in issue_id or "robots" in issue_id:
        return "crawl-policy"
    if "social" in issue_id:
        return "metadata"
    if "faq" in issue_id:
        return "answer-readiness"
    return "scanner-surface"


def _workflow_from_issue(issue: dict[str, Any]) -> str:
    severity = issue.get("severity", "medium")
    if severity == "high":
        return "executive review -> fix pack -> CI re-check"
    return "operator review -> backlog -> re-scan"


def _owner_from_issue(issue: dict[str, Any]) -> str:
    issue_id = str(issue.get("issue_id", ""))
    if any(item in issue_id for item in ["schema", "social", "faq"]):
        return "content_or_seo_owner"
    return "technical_seo_owner"


def _impact_from_severity(severity: str) -> str:
    return {
        "high": "high business and discoverability impact",
        "medium": "meaningful discoverability impact",
        "low": "small but compounding hygiene impact",
    }.get(severity, "meaningful discoverability impact")


def _severity_from_priority(finding: dict[str, Any]) -> str:
    score = float(finding.get("priority_score", 0) or 0)
    if score >= 80:
        return "high"
    if score >= 50:
        return "medium"
    return "low"


def _owner_from_finding(finding: dict[str, Any]) -> str:
    if "schema" in str(finding.get("title", "")).lower():
        return "technical_seo_owner"
    if "content" in str(finding.get("title", "")).lower():
        return "content_owner"
    return "operator"
