from __future__ import annotations

from typing import Any


def build_patch_pack(
    *,
    project: dict[str, Any],
    findings: list[dict[str, Any]],
    report_language: str,
    audience: str,
    review_mode: str,
) -> dict[str, Any]:
    top_findings = findings[:5]
    issue_backlog = []
    developer_briefs = []
    content_briefs = []
    schema_patches = []
    llms_suggestions = []
    for index, finding in enumerate(top_findings, start=1):
        title = finding.get("title") or f"Finding {index}"
        summary = finding.get("summary") or ""
        recommendation = finding.get("recommendation") or ""
        priority = finding.get("priority_label") or "planned"
        issue_backlog.append(
            {
                "title": title,
                "priority": priority,
                "summary": summary,
                "acceptance_criteria": recommendation,
            }
        )
        developer_briefs.append(
            {
                "title": title,
                "implementation_brief": recommendation,
                "risk_notes": finding.get("notes") or "Human review required.",
            }
        )
        content_briefs.append(
            {
                "title": title,
                "content_angle": summary,
                "editorial_direction": recommendation,
            }
        )
        schema_patches.append(
            {
                "title": f"{title} schema patch",
                "suggestion": f"Add or refine structured data related to: {summary}",
            }
        )
        llms_suggestions.append(
            {
                "title": f"{title} llms.txt improvement",
                "suggestion": f"Reflect the fix in AI-facing summaries for {project['website_url']}.",
            }
        )
    return {
        "project": project,
        "report_language": report_language,
        "audience": audience,
        "review_mode": review_mode,
        "issue_backlog": issue_backlog,
        "developer_briefs": developer_briefs,
        "content_briefs": content_briefs,
        "schema_patch_suggestions": schema_patches,
        "llms_txt_suggestions": llms_suggestions,
    }


def build_client_delivery_pack(
    *,
    project: dict[str, Any],
    report_language: str,
    audience: str,
    workspace_branding: dict[str, Any],
    reports: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    sov_runs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "project": project,
        "report_language": report_language,
        "audience": audience,
        "workspace_branding": workspace_branding,
        "delivery_summary": {
            "report_count": len(reports),
            "artifact_count": len(artifacts),
            "sov_run_count": len(sov_runs),
        },
        "report_pack": reports[:3],
        "artifact_pack": artifacts[:10],
        "sov_pack": sov_runs[:3],
        "one_click_deliverables": [
            "audit export",
            "llms.txt draft",
            "entity brief",
            "AI visibility report",
            "prioritized implementation pack",
        ],
    }
