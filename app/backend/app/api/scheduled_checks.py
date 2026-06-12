from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import ScheduledCheck, User
from ..schemas import ScheduledCheckCreate, ScheduledCheckRead
from ..services.scheduling import describe_schedule

router = APIRouter(prefix="/scheduled-checks", tags=["scheduled-checks"])


@router.get("", response_model=list[ScheduledCheckRead])
def list_scheduled_checks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ScheduledCheckRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(ScheduledCheck).filter(ScheduledCheck.project_id == project_id).all()
    )
    response: list[ScheduledCheckRead] = []
    for row in rows:
        config = json.loads(row.config_json)
        descriptor = describe_schedule(
            row.frequency, row.check_type, row.is_enabled, config, row.last_run_at
        )
        response.append(
            ScheduledCheckRead(
                id=row.id,
                workspace_id=row.workspace_id,
                project_id=row.project_id,
                name=row.name,
                frequency=row.frequency,
                check_type=row.check_type,
                is_enabled=row.is_enabled,
                last_run_at=row.last_run_at,
                config=config,
                schedule_mode=descriptor.schedule_mode,
                execution_path=descriptor.execution_path,
                next_run_hint=descriptor.next_run_hint,
                last_status=descriptor.last_status,
                limitations=descriptor.limitations,
                created_at=row.created_at,
            )
        )
    return response


@router.post("", response_model=ScheduledCheckRead)
def create_scheduled_check(
    payload: ScheduledCheckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduledCheckRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    config = {
        "schedule_mode": payload.config.get("schedule_mode", "cron"),
        "schedule_expression": payload.config.get(
            "schedule_expression", payload.frequency
        ),
        "target": payload.config.get("target", payload.check_type),
        "last_status": "queued" if payload.is_enabled else "disabled",
        **payload.config,
    }
    row = ScheduledCheck(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        name=payload.name,
        frequency=payload.frequency,
        check_type=payload.check_type,
        is_enabled=payload.is_enabled,
        config_json=json.dumps(config, ensure_ascii=False),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "scheduled_check.created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=project.id,
        metadata={
            "check_type": payload.check_type,
            "frequency": payload.frequency,
            "schedule_mode": config["schedule_mode"],
        },
    )
    db.commit()
    db.refresh(row)
    descriptor = describe_schedule(
        row.frequency, row.check_type, row.is_enabled, config, row.last_run_at
    )
    return ScheduledCheckRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        name=row.name,
        frequency=row.frequency,
        check_type=row.check_type,
        is_enabled=row.is_enabled,
        last_run_at=row.last_run_at,
        config=config,
        schedule_mode=descriptor.schedule_mode,
        execution_path=descriptor.execution_path,
        next_run_hint=descriptor.next_run_hint,
        last_status=descriptor.last_status,
        limitations=descriptor.limitations,
        created_at=row.created_at,
    )
