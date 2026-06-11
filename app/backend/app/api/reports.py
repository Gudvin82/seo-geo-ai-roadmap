from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Report, User
from ..schemas import ReportRead

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=list[ReportRead])
def list_reports(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ReportRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(Report)
        .filter(Report.project_id == project_id)
        .order_by(Report.id.desc())
        .all()
    )
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
