from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..metrics import SOV_RUNS
from ..models import Project, SovRun, User
from ..schemas import SovCheckRequest, SovRunRead

router = APIRouter(prefix="/sov", tags=["sov"])


def _estimate_share(query_count: int, provider_count: int) -> float:
    if not query_count or not provider_count:
        return 0.0
    raw = min(100, 35 + query_count * 7 + provider_count * 5)
    return round(raw / 100, 2)


def _serialize(row: SovRun) -> SovRunRead:
    return SovRunRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        brand=row.brand,
        queries=json.loads(row.queries_json or "[]"),
        providers=json.loads(row.providers_json or "[]"),
        results=json.loads(row.results_json or "[]"),
        mention_summary=row.mention_summary,
        share_estimate=row.share_estimate,
        notes=row.notes,
        status=row.status,
        report_language=row.report_language,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )


@router.post("/check", response_model=SovRunRead)
def sov_check(
    payload: SovCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SovRunRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="editor"
    )
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    providers = payload.providers or ["chatgpt", "perplexity", "gemini"]
    mentions = [
        {
            "query": query,
            "provider": provider,
            "brand": payload.brand,
            "mentioned": provider in {"perplexity", "gemini"},
            "share_estimate": round(1 / max(1, len(providers)), 2),
            "notes": "Transparent heuristic starter. Manual review still required.",
        }
        for query in payload.queries
        for provider in providers
    ]
    mention_summary = (
        f"{payload.brand} evaluated across {len(payload.queries)} queries and "
        f"{len(providers)} providers for project {project.name}."
    )
    row = SovRun(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        user_id=current_user.id,
        brand=payload.brand,
        queries_json=json.dumps(payload.queries, ensure_ascii=False),
        providers_json=json.dumps(providers, ensure_ascii=False),
        results_json=json.dumps(mentions, ensure_ascii=False),
        mention_summary=mention_summary,
        share_estimate=_estimate_share(len(payload.queries), len(providers)),
        notes=payload.notes
        or (
            "Experimental AI Share of Voice flow. Heuristic summary only; "
            "manual validation is still recommended."
        ),
        status="completed",
        report_language=payload.language or project.language,
        completed_at=datetime.utcnow(),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "sov.completed",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        metadata={"brand": payload.brand, "queries": payload.queries},
    )
    db.commit()
    db.refresh(row)
    SOV_RUNS.labels(status=row.status).inc()
    return _serialize(row)


@router.get("/history", response_model=list[SovRunRead])
def list_sov_runs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[SovRunRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(SovRun)
        .filter(SovRun.project_id == project_id)
        .order_by(SovRun.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.get("/{sov_run_id}", response_model=SovRunRead)
def get_sov_run(
    sov_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SovRunRead:
    row = db.get(SovRun, sov_run_id)
    project = db.get(Project, row.project_id) if row else None
    if not row or not project:
        raise HTTPException(status_code=404, detail="SOV run not found.")
    require_project_access(db, project.id, current_user, minimum_role="viewer")
    return _serialize(row)
