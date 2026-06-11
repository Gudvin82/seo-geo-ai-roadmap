from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Project, ScheduledCheck, User, Workspace
from ..schemas import ScheduledCheckCreate, ScheduledCheckRead

router = APIRouter(prefix="/scheduled-checks", tags=["scheduled-checks"])


def _project_for_user(db: Session, project_id: int, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    workspace = db.get(Workspace, project.workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.get("", response_model=list[ScheduledCheckRead])
def list_scheduled_checks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ScheduledCheckRead]:
    _project_for_user(db, project_id, current_user)
    rows = (
        db.query(ScheduledCheck).filter(ScheduledCheck.project_id == project_id).all()
    )
    return [
        ScheduledCheckRead(
            id=row.id,
            workspace_id=row.workspace_id,
            project_id=row.project_id,
            name=row.name,
            frequency=row.frequency,
            check_type=row.check_type,
            is_enabled=row.is_enabled,
            last_run_at=row.last_run_at,
            config=json.loads(row.config_json),
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.post("", response_model=ScheduledCheckRead)
def create_scheduled_check(
    payload: ScheduledCheckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduledCheckRead:
    _project_for_user(db, payload.project_id, current_user)
    row = ScheduledCheck(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        name=payload.name,
        frequency=payload.frequency,
        check_type=payload.check_type,
        is_enabled=payload.is_enabled,
        config_json=json.dumps(payload.config, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return ScheduledCheckRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        name=row.name,
        frequency=row.frequency,
        check_type=row.check_type,
        is_enabled=row.is_enabled,
        last_run_at=row.last_run_at,
        config=payload.config,
        created_at=row.created_at,
    )
