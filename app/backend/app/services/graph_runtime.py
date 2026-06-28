from __future__ import annotations

from datetime import datetime
from typing import Any

GRAPH_CONTRACT_VERSION = "v6.8.5"


def build_graph_from_scan_summary(
    scan_job_id: int, summary: dict[str, Any]
) -> dict[str, Any]:
    target_id = f"target-{scan_job_id}"
    nodes = [
        {
            "id": target_id,
            "label": summary.get("target_domain", "target"),
            "node_type": "target",
            "severity": None,
            "metadata": {"scan_mode": summary.get("scan_mode", "passive")},
        }
    ]
    edges = []
    filters = ["severity", "surface", "status"]
    for issue in summary.get("issues", []):
        issue_node = {
            "id": issue["issue_id"],
            "label": issue.get("title", issue["issue_id"]),
            "node_type": "issue",
            "severity": issue.get("severity"),
            "metadata": {"recommended_action": issue.get("recommended_action", "")},
        }
        nodes.append(issue_node)
        edges.append(
            {
                "source": target_id,
                "target": issue["issue_id"],
                "relationship": "has_issue",
            }
        )
        module_node_id = f"surface-{issue['issue_id']}"
        nodes.append(
            {
                "id": module_node_id,
                "label": _surface_label(issue["issue_id"]),
                "node_type": "surface",
                "severity": issue.get("severity"),
                "metadata": {},
            }
        )
        edges.append(
            {
                "source": issue["issue_id"],
                "target": module_node_id,
                "relationship": "affects_surface",
            }
        )
    return {
        "contract_version": GRAPH_CONTRACT_VERSION,
        "snapshot_id": f"scan-job-{scan_job_id}",
        "source_type": "scan_job",
        "source_id": str(scan_job_id),
        "generated_at": datetime.utcnow(),
        "nodes": _unique_nodes(nodes),
        "edges": edges,
        "filters": filters,
        "change_summary": ["Dynamic graph built from machine report JSON."],
    }


def build_graph_from_audit_findings(
    audit_run_id: int, findings: list[dict[str, Any]]
) -> dict[str, Any]:
    root_id = f"audit-{audit_run_id}"
    nodes = [
        {
            "id": root_id,
            "label": f"audit-run-{audit_run_id}",
            "node_type": "audit_run",
            "severity": None,
            "metadata": {"finding_count": len(findings)},
        }
    ]
    edges = []
    changes = []
    for index, finding in enumerate(findings, start=1):
        finding_id = f"finding-{audit_run_id}-{index}"
        priority = float(finding.get("priority_score", 0) or 0)
        severity = "high" if priority >= 80 else "medium" if priority >= 50 else "low"
        nodes.append(
            {
                "id": finding_id,
                "label": finding.get("title", f"Finding {index}"),
                "node_type": "finding",
                "severity": severity,
                "metadata": {
                    "priority_score": priority,
                    "benchmark_status": finding.get("benchmark_status", ""),
                },
            }
        )
        edges.append(
            {"source": root_id, "target": finding_id, "relationship": "contains"}
        )
        recommendation_id = f"recommendation-{audit_run_id}-{index}"
        nodes.append(
            {
                "id": recommendation_id,
                "label": finding.get("recommendation", "Review recommendation"),
                "node_type": "recommendation",
                "severity": severity,
                "metadata": {"status": "proposed"},
            }
        )
        edges.append(
            {
                "source": finding_id,
                "target": recommendation_id,
                "relationship": "resolved_by",
            }
        )
        changes.append(
            f"{finding.get('title', f'Finding {index}')} scored {priority:.0f}."
        )
    return {
        "contract_version": GRAPH_CONTRACT_VERSION,
        "snapshot_id": f"audit-run-{audit_run_id}",
        "source_type": "audit_run",
        "source_id": str(audit_run_id),
        "generated_at": datetime.utcnow(),
        "nodes": _unique_nodes(nodes),
        "edges": edges,
        "filters": ["severity", "priority_score", "benchmark_status"],
        "change_summary": changes or ["Dynamic graph built from audit findings."],
    }


def _surface_label(issue_id: str) -> str:
    if "schema" in issue_id:
        return "Structured data"
    if "social" in issue_id:
        return "Open Graph / Twitter"
    if "faq" in issue_id:
        return "FAQ / answer-ready"
    if "robots" in issue_id or "bot" in issue_id:
        return "Crawl and AI policy"
    return "Discoverability surface"


def _unique_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for node in nodes:
        deduped[node["id"]] = node
    return list(deduped.values())
