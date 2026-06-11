from __future__ import annotations

import json

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..config import load_settings
from ..database import get_db
from ..deps import get_current_user
from ..models import AuditRun, Project, User, Workspace
from ..schemas import AuditRunCreate, AuditRunRead
from ..services.audits import execute_audit_run_by_id
from ..services.presets import AUDIT_PRESETS

router = APIRouter(prefix="/audit-runs", tags=["audit-runs"])


def _project_for_user(db: Session, project_id: int, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    workspace = db.get(Workspace, project.workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.get("/presets")
def list_presets() -> dict:
    return {"presets": AUDIT_PRESETS}


@router.get("", response_model=list[AuditRunRead])
def list_audit_runs(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[AuditRunRead]:
    _project_for_user(db, project_id, current_user)
    rows = db.query(AuditRun).filter(AuditRun.project_id == project_id).order_by(AuditRun.id.desc()).all()
    return [
        AuditRunRead(
            id=row.id,
            project_id=row.project_id,
            workspace_id=row.workspace_id,
            status=row.status,
            report_language=row.report_language,
            selected_checks=json.loads(row.selected_checks_json),
            finding_groups=json.loads(row.finding_groups_json),
            summary_score=row.summary_score,
            created_at=row.created_at,
            completed_at=row.completed_at,
        )
        for row in rows
    ]


@router.post("", response_model=AuditRunRead)
def create_audit_run(
    payload: AuditRunCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AuditRunRead:
    project = _project_for_user(db, payload.project_id, current_user)
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(status_code=400, detail="Project and workspace do not match.")
    selected_checks = payload.selected_checks or AUDIT_PRESETS.get(project.audit_preset, [])
    row = AuditRun(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        user_id=current_user.id,
        status="queued",
        report_language=payload.report_language,
        selected_checks_json=json.dumps(selected_checks, ensure_ascii=False),
        finding_groups_json="[]",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    settings = getattr(request.app.state, "settings", load_settings())
    background_tasks.add_task(execute_audit_run_by_id, settings, row.id, payload.provider_config_id)
    return AuditRunRead(
        id=row.id,
        project_id=row.project_id,
        workspace_id=row.workspace_id,
        status=row.status,
        report_language=row.report_language,
        selected_checks=selected_checks,
        finding_groups=[],
        summary_score=row.summary_score,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )


@router.get("/{audit_run_id}", response_model=AuditRunRead)
def get_audit_run(audit_run_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> AuditRunRead:
    row = db.get(AuditRun, audit_run_id)
    if not row:
        raise HTTPException(status_code=404, detail="Audit run not found.")
    _project_for_user(db, row.project_id, current_user)
    return AuditRunRead(
        id=row.id,
        project_id=row.project_id,
        workspace_id=row.workspace_id,
        status=row.status,
        report_language=row.report_language,
        selected_checks=json.loads(row.selected_checks_json),
        finding_groups=json.loads(row.finding_groups_json),
        summary_score=row.summary_score,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )
