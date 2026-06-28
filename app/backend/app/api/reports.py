from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Report, User
from ..schemas import ReportAssistantRead, ReportAssistantRequest, ReportRead

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


@router.post("/{report_id}/assistant", response_model=ReportAssistantRead)
def ask_report_assistant(
    report_id: int,
    payload: ReportAssistantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportAssistantRead:
    row = db.get(Report, report_id)
    if not row:
        raise HTTPException(status_code=404, detail="Report not found.")
    require_project_access(db, row.project_id, current_user, minimum_role="viewer")
    summary = json.loads(row.summary_json or "{}")
    benchmark = summary.get("benchmark_summary", {})
    findings = summary.get("finding_groups", []) or summary.get("priorities", [])
    top_findings = findings[:3]
    if payload.language == "ru":
        answer = (
            "Короткий разбор отчета подготовлен в operator mode. "
            "Сначала сфокусируйтесь на самых приоритетных проблемах, затем перепроверьте изменения повторным аудитом."
        )
        limitations = [
            "Этот ответ построен по данным отчета и не является новым live-crawl.",
            "Перед публикацией правок нужен human review.",
        ]
    else:
        answer = (
            "This report answer was generated in operator mode from the stored audit payload. "
            "Start with the highest-priority fixes, then verify them with a fresh re-audit."
        )
        limitations = [
            "This answer is derived from the saved report payload, not a new live crawl.",
            "Human review is still required before publishing fixes.",
        ]
    key_points = [
        item.get("title", item.get("finding", "Priority finding"))
        for item in top_findings
        if isinstance(item, dict)
    ]
    follow_up_actions = [
        benchmark.get("next_step") if isinstance(benchmark, dict) else None,
        "Open the task bundle and assign owners for the highest-impact items.",
        "Run compare / re-audit after implementation to confirm the delta.",
    ]
    return ReportAssistantRead(
        report_id=row.id,
        contract_version="v6.7.5",
        answer=answer,
        key_points=[item for item in key_points if item],
        follow_up_actions=[item for item in follow_up_actions if item],
        limitations=limitations,
    )
