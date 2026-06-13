from __future__ import annotations

import json
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..access import require_project_access
from ..database import get_db
from ..deps import get_current_user, get_optional_current_user
from ..models import AuditRun, ScanJob, User
from ..schemas import GraphEdgeRead, GraphNodeRead, GraphSnapshotRead
from ..services import scan_jobs
from ..services.graph_runtime import (
    build_graph_from_audit_findings,
    build_graph_from_scan_summary,
)

router = APIRouter(prefix="/graph-runtime", tags=["graph-runtime"])


def _read_scan_summary(scan_job: ScanJob) -> dict:
    for artifact in json.loads(scan_job.report_artifacts_json or "[]"):
        if artifact.get("kind") == "machine_report":
            with open(artifact["path"], "r", encoding="utf-8") as handle:
                return json.load(handle)
    raise HTTPException(status_code=404, detail="Machine report artifact not found.")


@router.get("/scan-job/{scan_job_id}", response_model=GraphSnapshotRead)
def scan_graph_snapshot(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> GraphSnapshotRead:
    scan_job = db.get(ScanJob, scan_job_id)
    if not scan_job:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    scan_jobs.authorize_scan_job_access(
        scan_job, current_user, x_scanner_session
    )
    summary = _read_scan_summary(scan_job)
    payload = build_graph_from_scan_summary(scan_job.id, summary)
    return GraphSnapshotRead(
        contract_version=payload["contract_version"],
        snapshot_id=payload["snapshot_id"],
        source_type=payload["source_type"],
        source_id=payload["source_id"],
        generated_at=payload["generated_at"],
        nodes=[GraphNodeRead(**item) for item in payload["nodes"]],
        edges=[GraphEdgeRead(**item) for item in payload["edges"]],
        filters=payload["filters"],
        change_summary=payload["change_summary"],
    )


@router.get("/audit-run/{audit_run_id}", response_model=GraphSnapshotRead)
def audit_graph_snapshot(
    audit_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GraphSnapshotRead:
    audit_run = db.get(AuditRun, audit_run_id)
    if not audit_run:
        raise HTTPException(status_code=404, detail="Audit run not found.")
    require_project_access(
        db, audit_run.project_id, current_user, minimum_role="viewer"
    )
    findings = json.loads(audit_run.finding_groups_json or "[]")
    payload = build_graph_from_audit_findings(audit_run.id, findings)
    return GraphSnapshotRead(
        contract_version=payload["contract_version"],
        snapshot_id=payload["snapshot_id"],
        source_type=payload["source_type"],
        source_id=payload["source_id"],
        generated_at=payload["generated_at"],
        nodes=[GraphNodeRead(**item) for item in payload["nodes"]],
        edges=[GraphEdgeRead(**item) for item in payload["edges"]],
        filters=payload["filters"],
        change_summary=payload["change_summary"],
    )
