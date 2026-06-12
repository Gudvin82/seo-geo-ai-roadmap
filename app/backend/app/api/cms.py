from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import AuditRun, CmsConnector, User
from ..schemas import CmsConnectorCreate, CmsConnectorRead, PatchPackRead
from ..services.cms import cms_patch_package, inventory_cms

router = APIRouter(prefix="/cms", tags=["cms"])


def _serialize(row: CmsConnector) -> CmsConnectorRead:
    return CmsConnectorRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        cms_type=row.cms_type,
        label=row.label,
        base_url=row.base_url,
        auth_env_var=row.auth_env_var,
        writeback_mode=row.writeback_mode,
        last_inventory=json.loads(row.last_inventory_json or "{}"),
        last_sync_status=row.last_sync_status,
        last_sync_at=row.last_sync_at,
        created_at=row.created_at,
    )


@router.get("", response_model=list[CmsConnectorRead])
def list_cms_connectors(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CmsConnectorRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(CmsConnector)
        .filter(CmsConnector.project_id == project_id)
        .order_by(CmsConnector.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.post("", response_model=CmsConnectorRead)
def create_cms_connector(
    payload: CmsConnectorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CmsConnectorRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    row = CmsConnector(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        cms_type=payload.cms_type,
        label=payload.label,
        base_url=payload.base_url,
        auth_env_var=payload.auth_env_var,
        writeback_mode=payload.writeback_mode,
        last_inventory_json="{}",
        last_sync_status="created",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.post("/{connector_id}/inventory", response_model=CmsConnectorRead)
def sync_cms_inventory(
    connector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CmsConnectorRead:
    row = db.get(CmsConnector, connector_id)
    if not row:
        raise HTTPException(status_code=404, detail="CMS connector not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="editor")
    inventory = inventory_cms(row.cms_type, row.base_url, row.auth_env_var)
    row.last_inventory_json = json.dumps(inventory, ensure_ascii=False)
    row.last_sync_status = "completed"
    row.last_sync_at = datetime.utcnow()
    db.add(row)
    record_audit_log(
        db,
        "cms.inventory_synced",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"connector_id": row.id, "cms_type": row.cms_type},
    )
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.post("/{connector_id}/patch-package", response_model=PatchPackRead)
def generate_cms_patch_package(
    connector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatchPackRead:
    row = db.get(CmsConnector, connector_id)
    if not row:
        raise HTTPException(status_code=404, detail="CMS connector not found.")
    project, _ = require_project_access(
        db, row.project_id, current_user, minimum_role="editor"
    )
    latest_audit = (
        db.query(AuditRun)
        .filter(AuditRun.project_id == project.id)
        .order_by(AuditRun.id.desc())
        .first()
    )
    findings = (
        json.loads(latest_audit.finding_groups_json or "[]") if latest_audit else []
    )
    payload = cms_patch_package(
        row.cms_type,
        row.writeback_mode,
        project.name,
        project.website_url,
        findings,
    )
    return PatchPackRead(
        project_id=project.id,
        workspace_id=project.workspace_id,
        report_language=project.language,
        audience="agency",
        review_mode=row.writeback_mode,
        outputs=payload,
    )
