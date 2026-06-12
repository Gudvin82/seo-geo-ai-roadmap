from __future__ import annotations

import json

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access, require_workspace_access
from ..config import load_settings
from ..database import get_db
from ..deps import get_current_user
from ..metrics import AUDIT_RUNS
from ..models import AuditRun, User
from ..schemas import AuditRunAccepted, AuditRunCreate, AuditRunRead, AuditRunRequest
from ..services.audits import execute_audit_run_by_id
from ..services.presets import AUDIT_PRESETS

router = APIRouter(prefix="/audit-runs", tags=["audit-runs"])


def _serialize_audit_run(row: AuditRun) -> AuditRunRead:
    return AuditRunRead(
        id=row.id,
        project_id=row.project_id,
        workspace_id=row.workspace_id,
        status=row.status,
        report_language=row.report_language,
        mode=row.mode,
        market=row.market,
        target_url=row.target_url,
        selected_checks=json.loads(row.selected_checks_json),
        selected_providers=json.loads(row.provider_names_json or "[]"),
        accepted_parameters=json.loads(row.accepted_parameters_json or "{}"),
        finding_groups=json.loads(row.finding_groups_json),
        summary_score=row.summary_score,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )


@router.get("/presets")
def list_presets() -> dict:
    return {"presets": AUDIT_PRESETS}


@router.get("", response_model=list[AuditRunRead])
def list_audit_runs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AuditRunRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project_id)
        .order_by(AuditRun.id.desc())
        .all()
    )
    return [_serialize_audit_run(row) for row in rows]


@router.post("", response_model=AuditRunRead)
def create_audit_run(
    payload: AuditRunCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AuditRunRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    selected_checks = payload.selected_checks or AUDIT_PRESETS.get(
        project.audit_preset, []
    )
    row = AuditRun(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        user_id=current_user.id,
        status="queued",
        report_language=payload.report_language,
        mode="quick",
        market=project.market,
        target_url=project.website_url,
        selected_checks_json=json.dumps(selected_checks, ensure_ascii=False),
        provider_names_json="[]",
        accepted_parameters_json=json.dumps(
            {
                "workspace_id": payload.workspace_id,
                "project_id": payload.project_id,
                "selected_checks": selected_checks,
                "report_language": payload.report_language,
                "mode": "quick",
            },
            ensure_ascii=False,
        ),
        finding_groups_json="[]",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    settings = getattr(request.app.state, "settings", load_settings())
    background_tasks.add_task(
        execute_audit_run_by_id, settings, row.id, payload.provider_config_id
    )
    AUDIT_RUNS.labels(status=row.status).inc()
    record_audit_log(
        db,
        "audit.run_requested",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"selected_checks": selected_checks, "mode": "quick"},
    )
    db.commit()
    db.refresh(row)
    return _serialize_audit_run(row)


@router.post("/run", response_model=AuditRunAccepted)
def run_audit(
    payload: AuditRunRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AuditRunAccepted:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    selected_checks = payload.selected_checks or AUDIT_PRESETS.get(
        project.audit_preset, []
    )
    accepted_parameters = {
        "workspace_id": payload.workspace_id,
        "project_id": payload.project_id,
        "domain_or_url": payload.domain_or_url,
        "selected_checks": selected_checks,
        "selected_providers": payload.selected_providers,
        "report_language": payload.report_language,
        "market": payload.market or project.market,
        "mode": payload.mode,
        "brand_facts_profile_id": payload.brand_facts_profile_id,
    }
    row = AuditRun(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        user_id=current_user.id,
        status="queued",
        report_language=payload.report_language,
        mode=payload.mode,
        market=payload.market or project.market,
        target_url=payload.domain_or_url,
        selected_checks_json=json.dumps(selected_checks, ensure_ascii=False),
        provider_names_json=json.dumps(payload.selected_providers, ensure_ascii=False),
        accepted_parameters_json=json.dumps(accepted_parameters, ensure_ascii=False),
        finding_groups_json="[]",
    )
    db.add(row)
    db.flush()
    settings = getattr(request.app.state, "settings", load_settings())
    background_tasks.add_task(execute_audit_run_by_id, settings, row.id, None)
    AUDIT_RUNS.labels(status=row.status).inc()
    record_audit_log(
        db,
        "audit.run_requested",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata=accepted_parameters,
    )
    db.commit()
    return AuditRunAccepted(
        audit_job_id=row.id,
        initial_status=row.status,
        accepted_parameters=accepted_parameters,
        status_endpoint=f"/api/v1/audit-runs/{row.id}",
        report_endpoint=f"/api/v1/reports?project_id={row.project_id}",
        artifacts_endpoint=f"/api/v1/artifacts?project_id={row.project_id}",
    )


@router.get("/{audit_run_id}", response_model=AuditRunRead)
def get_audit_run(
    audit_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AuditRunRead:
    row = db.get(AuditRun, audit_run_id)
    if not row:
        raise HTTPException(status_code=404, detail="Audit run not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="viewer")
    return _serialize_audit_run(row)


@router.post("/{audit_run_id}/retry", response_model=AuditRunAccepted)
def retry_audit_run(
    audit_run_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AuditRunAccepted:
    source = db.get(AuditRun, audit_run_id)
    if not source:
        raise HTTPException(status_code=404, detail="Audit run not found.")
    project, _ = require_project_access(
        db, source.project_id, current_user, minimum_role="editor"
    )
    accepted_parameters = json.loads(source.accepted_parameters_json or "{}")
    row = AuditRun(
        workspace_id=source.workspace_id,
        project_id=source.project_id,
        user_id=current_user.id,
        status="queued",
        report_language=source.report_language,
        mode=source.mode,
        market=source.market or project.market,
        target_url=source.target_url or project.website_url,
        selected_checks_json=source.selected_checks_json,
        provider_names_json=source.provider_names_json,
        accepted_parameters_json=source.accepted_parameters_json,
        finding_groups_json="[]",
    )
    db.add(row)
    db.flush()
    settings = getattr(request.app.state, "settings", load_settings())
    background_tasks.add_task(execute_audit_run_by_id, settings, row.id, None)
    AUDIT_RUNS.labels(status=row.status).inc()
    record_audit_log(
        db,
        "audit.retry_requested",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"source_audit_run_id": source.id, **accepted_parameters},
    )
    db.commit()
    return AuditRunAccepted(
        audit_job_id=row.id,
        initial_status=row.status,
        accepted_parameters=accepted_parameters,
        status_endpoint=f"/api/v1/audit-runs/{row.id}",
        report_endpoint=f"/api/v1/reports?project_id={row.project_id}",
        artifacts_endpoint=f"/api/v1/artifacts?project_id={row.project_id}",
    )
