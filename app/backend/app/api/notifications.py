from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import NotificationEndpoint, User
from ..schemas import NotificationEndpointCreate, NotificationEndpointRead

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationEndpointRead])
def list_notification_endpoints(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[NotificationEndpointRead]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
    rows = (
        db.query(NotificationEndpoint)
        .filter(NotificationEndpoint.workspace_id == workspace_id)
        .order_by(NotificationEndpoint.id.desc())
        .all()
    )
    return [
        NotificationEndpointRead(
            id=row.id,
            workspace_id=row.workspace_id,
            channel_type=row.channel_type,
            label=row.label,
            target_url=row.target_url,
            events=json.loads(row.events_json or "[]"),
            is_enabled=row.is_enabled,
            retry_policy={
                "max_attempts": 3,
                "initial_delay_seconds": 0.5,
                "backoff_multiplier": 2.0,
                "terminal_state": "dead",
            },
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.post("", response_model=NotificationEndpointRead)
def create_notification_endpoint(
    payload: NotificationEndpointCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NotificationEndpointRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="admin"
    )
    row = NotificationEndpoint(
        workspace_id=payload.workspace_id,
        channel_type=payload.channel_type,
        label=payload.label,
        target_url=payload.target_url,
        events_json=json.dumps(payload.events, ensure_ascii=False),
        is_enabled=payload.is_enabled,
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "notifications.endpoint_created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        metadata={"channel_type": payload.channel_type, "label": payload.label},
    )
    db.commit()
    db.refresh(row)
    return NotificationEndpointRead(
        id=row.id,
        workspace_id=row.workspace_id,
        channel_type=row.channel_type,
        label=row.label,
        target_url=row.target_url,
        events=payload.events,
        is_enabled=row.is_enabled,
        retry_policy={
            "max_attempts": 3,
            "initial_delay_seconds": 0.5,
            "backoff_multiplier": 2.0,
            "terminal_state": "dead",
        },
        created_at=row.created_at,
    )
