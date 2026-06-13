from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import (
    AuditRun,
    NotificationEndpoint,
    ScanJob,
    ScheduledCheck,
    User,
)
from ..schemas import (
    AgentModeContractRead,
    AgentModeOverviewRead,
    AgentModeRunRead,
    AgentModeRunRequest,
    TaskItemRead,
)
from ..services.agent_mode import (
    agent_mode_contract,
    agent_mode_overview,
    build_agent_mode_run,
)

router = APIRouter(prefix="/agent-mode", tags=["agent-mode"])


@router.get("/contract", response_model=AgentModeContractRead)
def get_agent_mode_contract() -> AgentModeContractRead:
    payload = agent_mode_contract()
    return AgentModeContractRead(**payload)


@router.get("/overview", response_model=AgentModeOverviewRead)
def get_agent_mode_overview(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AgentModeOverviewRead:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project.id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    latest_scan = (
        db.query(ScanJob)
        .filter(ScanJob.normalized_url == project.website_url)
        .order_by(ScanJob.id.desc())
        .first()
    )
    scheduled_checks = (
        db.query(ScheduledCheck).filter(ScheduledCheck.project_id == project.id).all()
    )
    notification_endpoints = (
        db.query(NotificationEndpoint)
        .filter(NotificationEndpoint.workspace_id == project.workspace_id)
        .all()
    )
    payload = agent_mode_overview(
        project=project,
        latest_audit=latest_audit,
        latest_scan=latest_scan,
        scheduled_checks=scheduled_checks,
        notification_endpoints=notification_endpoints,
    )
    return AgentModeOverviewRead(**payload)


@router.post("/runs", response_model=AgentModeRunRead)
def create_agent_mode_run(
    payload: AgentModeRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AgentModeRunRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="viewer"
    )
    audit_run = None
    scan_job = None
    if payload.source_type == "scan_job":
        if payload.source_id is None:
            scan_job = (
                db.query(ScanJob)
                .filter(ScanJob.normalized_url == project.website_url)
                .order_by(ScanJob.id.desc())
                .first()
            )
        else:
            scan_job = db.get(ScanJob, payload.source_id)
        if scan_job is None:
            raise HTTPException(
                status_code=404, detail="No scan job is available for agent mode."
            )
    else:
        if payload.source_id is None:
            audit_run = (
                db.query(AuditRun)
                .filter(AuditRun.project_id == project.id)
                .order_by(AuditRun.id.desc())
                .first()
            )
        else:
            audit_run = db.get(AuditRun, payload.source_id)
        if audit_run is None:
            raise HTTPException(
                status_code=404, detail="No audit run is available for agent mode."
            )

    result = build_agent_mode_run(
        project=project,
        mode=payload.mode,
        source_type=payload.source_type,
        source_id=payload.source_id,
        benchmark=payload.benchmark,
        audit_run=audit_run,
        scan_job=scan_job,
    )
    return AgentModeRunRead(
        contract_version=result["contract_version"],
        mode=result["mode"],
        project_id=result["project_id"],
        source_type=result["source_type"],
        source_id=result["source_id"],
        benchmark=result["benchmark"],
        summary=result["summary"],
        recommendations=result["recommendations"],
        alerts=result["alerts"],
        follow_up_tasks=[TaskItemRead(**item) for item in result["follow_up_tasks"]],
        safe_actions=result["safe_actions"],
        approval_required_for=result["approval_required_for"],
    )
