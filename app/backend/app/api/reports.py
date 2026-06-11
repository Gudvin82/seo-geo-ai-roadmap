from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Project, Report, User, Workspace
from ..schemas import ReportRead

router = APIRouter(prefix="/reports", tags=["reports"])


def _project_for_user(db: Session, project_id: int, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    workspace = db.get(Workspace, project.workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.get("", response_model=list[ReportRead])
def list_reports(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[ReportRead]:
    _project_for_user(db, project_id, current_user)
    rows = db.query(Report).filter(Report.project_id == project_id).order_by(Report.id.desc()).all()
    return [
        ReportRead(
            id=row.id,
            audit_run_id=row.audit_run_id,
            project_id=row.project_id,
            language=row.language,
            format=row.format,
            summary_markdown=row.summary_markdown,
            summary_json=json.loads(row.summary_json),
            created_at=row.created_at,
        )
        for row in rows
    ]
