from __future__ import annotations

import json
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user, get_optional_current_user
from ..models import AuditRun, Project, ScanJob, User
from ..schemas import TaskBundleRead, TaskExportRead, TaskExportRequest, TaskItemRead
from ..services import scan_jobs
from ..services.task_center import (
    build_task_bundle_from_audit_run,
    build_task_bundle_from_scan_job,
    export_bundle,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _scan_job_for_access(
    db: Session,
    scan_job_id: int,
    current_user: Optional[User],
    session_id: Optional[str],
) -> ScanJob:
    row = db.get(ScanJob, scan_job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan job not found.")
    scan_jobs.authorize_scan_job_access(row, current_user, session_id)
    if current_user is None:
        return row
    project = (
        db.query(Project)
        .filter(Project.website_url.like(f"%{row.target_domain}%"))
        .order_by(Project.id.desc())
        .first()
    )
    if project is not None:
        require_project_access(db, project.id, current_user, minimum_role="viewer")
    return row


def _load_scan_summary(scan_job: ScanJob) -> dict:
    for artifact in json.loads(scan_job.report_artifacts_json or "[]"):
        if artifact.get("kind") == "machine_report":
            try:
                with open(artifact["path"], "r", encoding="utf-8") as handle:
                    return json.load(handle)
            except FileNotFoundError as exc:
                raise HTTPException(
                    status_code=404, detail="Machine report artifact not found."
                ) from exc
    raise HTTPException(status_code=404, detail="Machine report artifact not found.")


@router.get("/scan-job/{scan_job_id}", response_model=TaskBundleRead)
def tasks_for_scan_job(
    scan_job_id: int,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> TaskBundleRead:
    scan_job = _scan_job_for_access(db, scan_job_id, current_user, x_scanner_session)
    summary = _load_scan_summary(scan_job)
    bundle = build_task_bundle_from_scan_job(scan_job, summary)
    return TaskBundleRead(
        contract_version=bundle["contract_version"],
        source_type=bundle["source_type"],
        source_id=bundle["source_id"],
        generated_at=bundle["generated_at"],
        summary=bundle["summary"],
        tasks=[TaskItemRead(**item) for item in bundle["tasks"]],
        markdown_ready=bundle["markdown_ready"],
        client_ready_summary=bundle["client_ready_summary"],
    )


@router.get("/audit-run/{audit_run_id}", response_model=TaskBundleRead)
def tasks_for_audit_run(
    audit_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskBundleRead:
    audit_run = db.get(AuditRun, audit_run_id)
    if not audit_run:
        raise HTTPException(status_code=404, detail="Audit run not found.")
    require_project_access(
        db, audit_run.project_id, current_user, minimum_role="viewer"
    )
    findings = json.loads(audit_run.finding_groups_json or "[]")
    bundle = build_task_bundle_from_audit_run(audit_run, findings)
    return TaskBundleRead(
        contract_version=bundle["contract_version"],
        source_type=bundle["source_type"],
        source_id=bundle["source_id"],
        generated_at=bundle["generated_at"],
        summary=bundle["summary"],
        tasks=[TaskItemRead(**item) for item in bundle["tasks"]],
        markdown_ready=bundle["markdown_ready"],
        client_ready_summary=bundle["client_ready_summary"],
    )


@router.post("/export", response_model=TaskExportRead)
def export_tasks(
    payload: TaskExportRequest,
    x_scanner_session: Optional[str] = Header(default=None, alias="X-Scanner-Session"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskExportRead:
    if payload.source_type == "scan_job":
        scan_job = _scan_job_for_access(
            db, payload.source_id, current_user, x_scanner_session
        )
        bundle = build_task_bundle_from_scan_job(scan_job, _load_scan_summary(scan_job))
        project_id = None
    else:
        audit_run = db.get(AuditRun, payload.source_id)
        if not audit_run:
            raise HTTPException(status_code=404, detail="Audit run not found.")
        require_project_access(
            db, audit_run.project_id, current_user, minimum_role="editor"
        )
        bundle = build_task_bundle_from_audit_run(
            audit_run, json.loads(audit_run.finding_groups_json or "[]")
        )
        project_id = audit_run.project_id

    result = export_bundle(
        bundle,
        payload.target,
        repository=payload.repository,
        token_env_var=payload.token_env_var,
        dry_run=payload.dry_run,
    )
    record_audit_log(
        db,
        "tasks.exported",
        user_id=current_user.id,
        project_id=project_id,
        metadata={
            "target": payload.target,
            "source_type": payload.source_type,
            "source_id": payload.source_id,
            "dry_run": payload.dry_run,
        },
    )
    db.commit()
    return TaskExportRead(**result)
