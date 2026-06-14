from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import EvidenceRecord, ExperimentRecord, User
from ..schemas import (
    EvidenceRecordCreate,
    EvidenceRecordRead,
    ExperimentRecordCreate,
    ExperimentRecordRead,
)

router = APIRouter(prefix="/proof", tags=["proof"])


def _serialize_evidence(row: EvidenceRecord) -> EvidenceRecordRead:
    return EvidenceRecordRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        label_type=row.label_type,
        title=row.title,
        summary=row.summary,
        source_ref=row.source_ref,
        links=json.loads(row.links_json or "[]"),
        created_at=row.created_at,
    )


def _serialize_experiment(row: ExperimentRecord) -> ExperimentRecordRead:
    return ExperimentRecordRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        source_type=row.source_type,
        source_id=row.source_id,
        change_summary=row.change_summary,
        confidence_label=row.confidence_label,
        before_snapshot=json.loads(row.before_snapshot_json or "{}"),
        after_snapshot=json.loads(row.after_snapshot_json or "{}"),
        evidence_links=json.loads(row.evidence_links_json or "[]"),
        outcome_metrics=json.loads(row.outcome_metrics_json or "{}"),
        created_at=row.created_at,
    )


@router.get("/labels")
def evidence_labels() -> dict:
    return {
        "labels": [
            "public_fact",
            "bounded_rollout_record",
            "internal_evidence",
            "demo_fixture",
            "synthetic_example",
        ],
        "confidence_labels": ["weak", "partial", "strong"],
    }


@router.get("/evidence", response_model=list[EvidenceRecordRead])
def list_evidence(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[EvidenceRecordRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(EvidenceRecord)
        .filter(EvidenceRecord.project_id == project_id)
        .order_by(EvidenceRecord.id.desc())
        .all()
    )
    return [_serialize_evidence(row) for row in rows]


@router.post("/evidence", response_model=EvidenceRecordRead)
def create_evidence(
    payload: EvidenceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EvidenceRecordRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    row = EvidenceRecord(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        label_type=payload.label_type,
        title=payload.title,
        summary=payload.summary,
        source_ref=payload.source_ref,
        links_json=json.dumps(payload.links, ensure_ascii=False),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "proof.evidence_created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=project.id,
        metadata={"label_type": row.label_type, "title": row.title},
    )
    db.commit()
    db.refresh(row)
    return _serialize_evidence(row)


@router.get("/experiments", response_model=list[ExperimentRecordRead])
def list_experiments(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ExperimentRecordRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(ExperimentRecord)
        .filter(ExperimentRecord.project_id == project_id)
        .order_by(ExperimentRecord.id.desc())
        .all()
    )
    return [_serialize_experiment(row) for row in rows]


@router.post("/experiments", response_model=ExperimentRecordRead)
def create_experiment(
    payload: ExperimentRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExperimentRecordRead:
    project, _ = require_project_access(
        db, payload.project_id, current_user, minimum_role="editor"
    )
    row = ExperimentRecord(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        source_type=payload.source_type,
        source_id=payload.source_id,
        change_summary=payload.change_summary,
        confidence_label=payload.confidence_label,
        before_snapshot_json=json.dumps(payload.before_snapshot, ensure_ascii=False),
        after_snapshot_json=json.dumps(payload.after_snapshot, ensure_ascii=False),
        evidence_links_json=json.dumps(payload.evidence_links, ensure_ascii=False),
        outcome_metrics_json=json.dumps(payload.outcome_metrics, ensure_ascii=False),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "proof.experiment_created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=project.id,
        metadata={"source_type": row.source_type, "source_id": row.source_id},
    )
    db.commit()
    db.refresh(row)
    return _serialize_experiment(row)
