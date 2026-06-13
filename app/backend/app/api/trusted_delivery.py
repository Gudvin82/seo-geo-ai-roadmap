from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import TrustedDeliveryTarget, User
from ..schemas import TrustedDeliveryTargetCreate, TrustedDeliveryTargetRead

router = APIRouter(prefix="/trusted-delivery-targets", tags=["trusted-delivery"])


def _serialize(row: TrustedDeliveryTarget) -> TrustedDeliveryTargetRead:
    return TrustedDeliveryTargetRead(
        id=row.id,
        workspace_id=row.workspace_id,
        label=row.label,
        repository=row.repository,
        base_branch=row.base_branch,
        allowed_domains=json.loads(row.allowed_domains_json or "[]"),
        auto_merge_mode=row.auto_merge_mode,
        required_checks=json.loads(row.required_checks_json or "[]"),
        is_enabled=row.is_enabled,
        created_at=row.created_at,
    )


@router.get("", response_model=list[TrustedDeliveryTargetRead])
def list_trusted_delivery_targets(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TrustedDeliveryTargetRead]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
    rows = (
        db.query(TrustedDeliveryTarget)
        .filter(TrustedDeliveryTarget.workspace_id == workspace_id)
        .order_by(TrustedDeliveryTarget.id.desc())
        .all()
    )
    return [_serialize(row) for row in rows]


@router.post("", response_model=TrustedDeliveryTargetRead)
def create_trusted_delivery_target(
    payload: TrustedDeliveryTargetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TrustedDeliveryTargetRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="admin"
    )
    if "/" not in payload.repository:
        raise HTTPException(
            status_code=400, detail="Repository must look like owner/name."
        )
    row = TrustedDeliveryTarget(
        workspace_id=payload.workspace_id,
        label=payload.label,
        repository=payload.repository.strip(),
        base_branch=payload.base_branch.strip() or "main",
        allowed_domains_json=json.dumps(payload.allowed_domains, ensure_ascii=False),
        auto_merge_mode=payload.auto_merge_mode,
        required_checks_json=json.dumps(payload.required_checks, ensure_ascii=False),
        is_enabled=payload.is_enabled,
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "trusted_delivery.target_created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        metadata={
            "repository": payload.repository,
            "auto_merge_mode": payload.auto_merge_mode,
        },
    )
    db.commit()
    db.refresh(row)
    return _serialize(row)
