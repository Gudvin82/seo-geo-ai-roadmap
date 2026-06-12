from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import IntegrationConnection, User
from ..schemas import IntegrationConnectionCreate, IntegrationConnectionRead
from ..services.integrations import compact_integration_summary, sync_integration_source

router = APIRouter(prefix="/integrations", tags=["integrations"])


def _serialize(row: IntegrationConnection) -> IntegrationConnectionRead:
    return IntegrationConnectionRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        source_type=row.source_type,
        label=row.label,
        property_identifier=row.property_identifier,
        credentials_env_var=row.credentials_env_var,
        config=json.loads(row.config_json or "{}"),
        latest_snapshot=json.loads(row.latest_snapshot_json or "{}"),
        last_sync_status=row.last_sync_status,
        last_sync_at=row.last_sync_at,
        created_at=row.created_at,
    )


@router.get("", response_model=list[IntegrationConnectionRead])
def list_integrations(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[IntegrationConnectionRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(IntegrationConnection)
        .filter(IntegrationConnection.project_id == project_id)
        .order_by(IntegrationConnection.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.post("", response_model=IntegrationConnectionRead)
def create_integration(
    payload: IntegrationConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationConnectionRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    if project.workspace_id != payload.workspace_id:
        raise HTTPException(
            status_code=400, detail="Project and workspace do not match."
        )
    row = IntegrationConnection(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        source_type=payload.source_type,
        label=payload.label,
        property_identifier=payload.property_identifier,
        credentials_env_var=payload.credentials_env_var,
        config_json=json.dumps(payload.config, ensure_ascii=False),
        latest_snapshot_json="{}",
        last_sync_status="created",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    record_audit_log(
        db,
        "integration.created",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"source_type": row.source_type, "label": row.label},
    )
    db.commit()
    return _serialize(row)


@router.post("/{integration_id}/sync", response_model=IntegrationConnectionRead)
def sync_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IntegrationConnectionRead:
    row = db.get(IntegrationConnection, integration_id)
    if not row:
        raise HTTPException(status_code=404, detail="Integration not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="editor")
    snapshot = sync_integration_source(row.source_type)
    snapshot["summary"] = compact_integration_summary(snapshot)
    row.latest_snapshot_json = json.dumps(snapshot, ensure_ascii=False)
    row.last_sync_status = "completed"
    row.last_sync_at = datetime.utcnow()
    db.add(row)
    record_audit_log(
        db,
        "integration.synced",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        metadata={"integration_id": row.id, "source_type": row.source_type},
    )
    db.commit()
    db.refresh(row)
    return _serialize(row)
