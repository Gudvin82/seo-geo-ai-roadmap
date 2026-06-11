from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import AuditLog, User
from ..schemas import AuditLogRead

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AuditLogRead]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
    rows = (
        db.query(AuditLog)
        .filter(AuditLog.workspace_id == workspace_id)
        .order_by(AuditLog.id.desc())
        .limit(100)
        .all()
    )
    return [
        AuditLogRead(
            id=row.id,
            event_type=row.event_type,
            user_id=row.user_id,
            workspace_id=row.workspace_id,
            project_id=row.project_id,
            metadata=json.loads(row.metadata_json or "{}"),
            created_at=row.created_at,
        )
        for row in rows
    ]
