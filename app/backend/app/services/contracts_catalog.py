from __future__ import annotations

from typing import Any


def contracts_catalog() -> list[dict[str, Any]]:
    return [
        {
            "id": "audit_run",
            "path": "contracts/audit-run.schema.json",
            "purpose": "Machine-readable audit output for app, agents, and CI.",
        },
        {
            "id": "task_bundle",
            "path": "contracts/task-bundle.schema.json",
            "purpose": "Normalized finding-to-task contract and export payload.",
        },
        {
            "id": "graph_snapshot",
            "path": "contracts/graph-snapshot.schema.json",
            "purpose": "Dynamic graph intelligence snapshot.",
        },
        {
            "id": "report_export",
            "path": "contracts/report-export.schema.json",
            "purpose": "Structured report and deliverable export contract.",
        },
        {
            "id": "command_contract",
            "path": "contracts/command-contract.schema.json",
            "purpose": "Machine-readable command and routing surface.",
        },
        {
            "id": "integration_contract",
            "path": "contracts/integration-contract.schema.json",
            "purpose": "Integration and CMS contract surface for app and CI flows.",
        },
        {
            "id": "product_modes",
            "path": "contracts/product-modes.schema.json",
            "purpose": "Machine-readable separation between repo, app, and scanner surfaces.",
        },
        {
            "id": "agent_mode",
            "path": "contracts/agent-mode.schema.json",
            "purpose": "Approval-bound agent orchestration contract.",
        },
    ]
