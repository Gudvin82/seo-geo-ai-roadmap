from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Artifact, AuditRun, Project, Report, SovRun, User, Workspace
from ..schemas import PatchPackRead, PatchPackRequest
from ..services.delivery import build_client_delivery_pack, build_patch_pack

router = APIRouter(prefix="/deliverables", tags=["deliverables"])


def _latest_audit(
    db: Session, project_id: int, audit_run_id: int | None
) -> AuditRun | None:
    if audit_run_id is not None:
        return db.get(AuditRun, audit_run_id)
    return (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project_id)
        .order_by(AuditRun.id.desc())
        .first()
    )


def _write_artifact(
    db: Session,
    *,
    project: Project,
    audit_run: AuditRun,
    artifact_type: str,
    payload: dict,
) -> Artifact:
    artifact_root = Path(getattr(db.bind.url, "database", "") or ".")
    output_dir = artifact_root.parent / "deliverables"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{artifact_type}-{project.id}.json"
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    row = Artifact(
        audit_run_id=audit_run.id,
        project_id=project.id,
        artifact_type=artifact_type,
        format="json",
        file_path=str(output_path),
        metadata_json=json.dumps(
            {"generated": True, "artifact_type": artifact_type}, ensure_ascii=False
        ),
    )
    db.add(row)
    return row


@router.post("/patch-pack", response_model=PatchPackRead)
def generate_patch_pack(
    payload: PatchPackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatchPackRead:
    project, workspace_access = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    audit_run = _latest_audit(db, project.id, payload.audit_run_id)
    if not audit_run:
        raise HTTPException(
            status_code=400,
            detail="Run at least one audit before generating a patch pack.",
        )
    findings = json.loads(audit_run.finding_groups_json or "[]") if audit_run else []
    pack = build_patch_pack(
        project={
            "id": project.id,
            "name": project.name,
            "website_url": project.website_url,
            "market": project.market,
            "language": project.language,
        },
        findings=findings,
        report_language=payload.report_language,
        audience=payload.audience,
        review_mode=payload.mode,
    )
    _write_artifact(
        db,
        project=project,
        audit_run=audit_run,
        artifact_type="patch_pack",
        payload=pack,
    )
    record_audit_log(
        db,
        "deliverable.patch_pack_generated",
        user_id=current_user.id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        metadata={"audience": payload.audience, "review_mode": payload.mode},
    )
    db.commit()
    return PatchPackRead(
        project_id=project.id,
        workspace_id=project.workspace_id,
        report_language=payload.report_language,
        audience=payload.audience,
        review_mode=payload.mode,
        outputs=pack,
    )


@router.post("/client-pack", response_model=PatchPackRead)
def generate_client_pack(
    payload: PatchPackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatchPackRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    audit_run = _latest_audit(db, project.id, payload.audit_run_id)
    if not audit_run:
        raise HTTPException(
            status_code=400,
            detail="Run at least one audit before generating a client pack.",
        )
    reports = (
        db.query(Report)
        .filter(Report.project_id == project.id)
        .order_by(Report.id.desc())
        .all()
    )
    artifacts = (
        db.query(Artifact)
        .filter(Artifact.project_id == project.id)
        .order_by(Artifact.id.desc())
        .all()
    )
    sov_runs = (
        db.query(SovRun)
        .filter(SovRun.project_id == project.id)
        .order_by(SovRun.id.desc())
        .all()
    )
    workspace = db.get(Workspace, project.workspace_id)
    branding = {
        "client_report_title": getattr(workspace, "client_report_title", None),
        "client_report_subtitle": getattr(workspace, "client_report_subtitle", None),
        "client_report_footer": getattr(workspace, "client_report_footer", None),
        "branding_logo_url": getattr(workspace, "branding_logo_url", None),
    }
    pack = build_client_delivery_pack(
        project={
            "id": project.id,
            "name": project.name,
            "website_url": project.website_url,
            "market": project.market,
            "language": project.language,
        },
        report_language=payload.report_language,
        audience=payload.audience,
        workspace_branding=branding,
        reports=[
            {"id": row.id, "language": row.language, "format": row.format}
            for row in reports
        ],
        artifacts=[
            {"id": row.id, "artifact_type": row.artifact_type, "format": row.format}
            for row in artifacts
        ],
        sov_runs=[
            {"id": row.id, "brand": row.brand, "share_estimate": row.share_estimate}
            for row in sov_runs
        ],
    )
    _write_artifact(
        db,
        project=project,
        audit_run=audit_run,
        artifact_type="client_delivery_pack",
        payload=pack,
    )
    record_audit_log(
        db,
        "deliverable.client_pack_generated",
        user_id=current_user.id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        metadata={"audience": payload.audience, "review_mode": payload.mode},
    )
    db.commit()
    return PatchPackRead(
        project_id=project.id,
        workspace_id=project.workspace_id,
        report_language=payload.report_language,
        audience=payload.audience,
        review_mode=payload.mode,
        outputs=pack,
    )
