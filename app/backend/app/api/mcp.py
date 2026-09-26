"""Stateless Streamable HTTP MCP surface for authenticated project reads."""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from ..access import require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import (
    AiVisibilitySnapshot,
    AuditRun,
    EvidenceRecord,
    IntegrationConnection,
    Project,
    ProjectResearchContext,
    User,
)
from ..services.geo_intelligence import build_unified_report
from ..services.graph_runtime import build_graph_from_audit_findings
from ..services.task_center import build_task_bundle_from_audit_run
from ..version import APP_VERSION

router = APIRouter(tags=["mcp"])
MCP_PROTOCOL_VERSION = "2025-03-26"

TOOLS = [
    {
        "name": "get_project_context",
        "description": "Read the authenticated project's market, language, competitors, goals, key pages, and seed keywords.",
        "inputSchema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer"}},
            "required": ["project_id"],
        },
    },
    {
        "name": "get_latest_unified_report",
        "description": "Read the latest completed unified audit report, evidence-backed findings, graph, and generated task bundle for a project.",
        "inputSchema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer"}},
            "required": ["project_id"],
        },
    },
    {
        "name": "list_project_evidence",
        "description": "Read recent evidence records for a project, including provider, market, language, observed time, cost, provenance, and cached research summaries.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100},
            },
            "required": ["project_id"],
        },
    },
    {
        "name": "list_connected_sources",
        "description": "Read current integration snapshots and sync status for a project. This tool never starts a provider request.",
        "inputSchema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer"}},
            "required": ["project_id"],
        },
    },
    {
        "name": "list_ai_visibility_history",
        "description": "Read saved AI visibility snapshots for a project without running model queries.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100},
            },
            "required": ["project_id"],
        },
    },
]


def _jsonrpc(
    request_id: Any, result: dict[str, Any], status_code: int = 200
) -> JSONResponse:
    return JSONResponse(
        {"jsonrpc": "2.0", "id": request_id, "result": result},
        status_code=status_code,
        headers={"MCP-Protocol-Version": MCP_PROTOCOL_VERSION},
    )


def _error(request_id: Any, code: int, message: str) -> JSONResponse:
    return JSONResponse(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        },
        headers={"MCP-Protocol-Version": MCP_PROTOCOL_VERSION},
    )


def _project(db: Session, project_id: int, user: User) -> Project:
    project, _ = require_project_access(db, project_id, user, minimum_role="viewer")
    return project


def _tool_data(
    name: str, arguments: dict[str, Any], db: Session, user: User
) -> dict[str, Any]:
    project_id = int(arguments.get("project_id", 0))
    if project_id <= 0:
        raise ValueError("project_id must be a positive integer.")
    project = _project(db, project_id, user)

    if name == "get_project_context":
        context = (
            db.query(ProjectResearchContext)
            .filter(ProjectResearchContext.project_id == project.id)
            .first()
        )
        return {
            "project_id": project.id,
            "name": project.name,
            "website_url": project.website_url,
            "market": project.market,
            "language": project.language,
            **(
                context.model_values()
                if context
                else {
                    "competitors": [],
                    "goals": [],
                    "key_pages": [],
                    "seed_keywords": [],
                }
            ),
            "updated_at": context.updated_at.isoformat() if context else None,
        }

    if name == "get_latest_unified_report":
        audit_run = (
            db.query(AuditRun)
            .filter(AuditRun.project_id == project.id, AuditRun.status == "completed")
            .order_by(AuditRun.completed_at.desc(), AuditRun.id.desc())
            .first()
        )
        if not audit_run:
            return {
                "project_id": project.id,
                "status": "insufficient_data",
                "report": None,
            }
        findings = json.loads(audit_run.finding_groups_json or "[]")
        report = build_unified_report(
            target_url=audit_run.target_url or "", findings=findings
        )
        report["tasks"] = build_task_bundle_from_audit_run(
            audit_run, report["findings"]
        )
        report["graph"] = build_graph_from_audit_findings(
            audit_run.id, report["findings"]
        )
        report["source"] = {"type": "audit_run", "id": audit_run.id}
        return report

    if name == "list_project_evidence":
        limit = min(max(int(arguments.get("limit", 25)), 1), 100)
        rows = (
            db.query(EvidenceRecord)
            .filter(EvidenceRecord.project_id == project.id)
            .order_by(EvidenceRecord.created_at.desc())
            .limit(limit)
            .all()
        )
        return {
            "project_id": project.id,
            "items": [
                {
                    "id": row.id,
                    "label_type": row.label_type,
                    "title": row.title,
                    "summary": (row.summary or "")[:4000],
                    "summary_truncated": len(row.summary or "") > 4000,
                    "source_ref": row.source_ref,
                    "created_at": row.created_at.isoformat(),
                }
                for row in rows
            ],
        }

    if name == "list_connected_sources":
        rows = (
            db.query(IntegrationConnection)
            .filter(IntegrationConnection.project_id == project.id)
            .order_by(IntegrationConnection.source_type.asc())
            .all()
        )
        items = []
        for row in rows:
            snapshot = json.loads(row.latest_snapshot_json or "{}")
            provider_rows = snapshot.get("rows")
            if isinstance(provider_rows, list) and len(provider_rows) > 10:
                snapshot["rows_truncated_count"] = len(provider_rows) - 10
                snapshot["rows"] = provider_rows[:10]
            items.append(
                {
                    "source_type": row.source_type,
                    "label": row.label,
                    "last_sync_status": row.last_sync_status,
                    "last_sync_at": row.last_sync_at.isoformat()
                    if row.last_sync_at
                    else None,
                    "snapshot": snapshot,
                }
            )
        return {
            "project_id": project.id,
            "items": items,
            "read_only": True,
            "provider_requests_started": False,
        }

    if name == "list_ai_visibility_history":
        limit = min(max(int(arguments.get("limit", 25)), 1), 100)
        rows = (
            db.query(AiVisibilitySnapshot)
            .filter(AiVisibilitySnapshot.project_id == project.id)
            .order_by(AiVisibilitySnapshot.observed_at.desc())
            .limit(limit)
            .all()
        )
        return {
            "project_id": project.id,
            "items": [
                {
                    "target_url": row.target_url,
                    "query": row.query,
                    "query_set": row.query_set,
                    "provider": row.provider,
                    "model": row.model,
                    "evidence_type": row.evidence_type,
                    "confidence": row.confidence,
                    "response_reference": row.response_reference,
                    "evidence": json.loads(row.evidence_json or "{}"),
                    "snapshot": json.loads(row.snapshot_json or "{}"),
                    "observed_at": row.observed_at.isoformat(),
                }
                for row in rows
            ],
        }
    raise ValueError(f"Unknown tool '{name}'.")


@router.post("/mcp")
def streamable_http_mcp(
    payload: dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """MCP JSON-RPC endpoint; all exposed tools are authenticated, project-scoped reads."""
    request_id = payload.get("id")
    method = payload.get("method")
    if payload.get("jsonrpc") != "2.0" or not isinstance(method, str):
        return _error(request_id, -32600, "Invalid JSON-RPC request.")
    if method == "notifications/initialized":
        return Response(status_code=202)
    if method == "initialize":
        return _jsonrpc(
            request_id,
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "seo-geo-ai-roadmap", "version": APP_VERSION},
            },
        )
    if method == "ping":
        return _jsonrpc(request_id, {})
    if method == "tools/list":
        return _jsonrpc(request_id, {"tools": TOOLS})
    if method == "tools/call":
        params = payload.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            return _error(request_id, -32602, "Tool arguments must be an object.")
        try:
            data = _tool_data(str(name), arguments, db, current_user)
        except ValueError as exc:
            result = {"isError": True, "content": [{"type": "text", "text": str(exc)}]}
            return _jsonrpc(request_id, result)
        except Exception as exc:
            from fastapi import HTTPException

            if isinstance(exc, HTTPException):
                result = {
                    "isError": True,
                    "content": [{"type": "text", "text": exc.detail}],
                }
                return _jsonrpc(request_id, result)
            raise
        return _jsonrpc(
            request_id,
            {
                "isError": False,
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(data, ensure_ascii=False, default=str),
                    }
                ],
                "structuredContent": data,
            },
        )
    return _error(request_id, -32601, "Method not found.")
