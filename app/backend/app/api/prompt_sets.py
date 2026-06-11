from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import PromptSet, User
from ..schemas import PromptSetCreate, PromptSetRead

router = APIRouter(prefix="/prompt-sets", tags=["prompts"])


@router.get("", response_model=list[PromptSetRead])
def list_prompt_sets(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PromptSetRead]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    rows = db.query(PromptSet).filter(PromptSet.workspace_id == workspace_id).all()
    return [
        PromptSetRead(
            id=row.id,
            workspace_id=row.workspace_id,
            name=row.name,
            description=row.description,
            purpose=row.purpose,
            output_format=row.output_format,
            model_recommendation=row.model_recommendation,
            risk_notes=row.risk_notes,
            human_review_required=row.human_review_required,
            prompt_items=json.loads(row.prompt_items_json),
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.post("", response_model=PromptSetRead)
def create_prompt_set(
    payload: PromptSetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PromptSetRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="editor"
    )
    row = PromptSet(
        workspace_id=payload.workspace_id,
        name=payload.name,
        description=payload.description,
        purpose=payload.purpose,
        output_format=payload.output_format,
        model_recommendation=payload.model_recommendation,
        risk_notes=payload.risk_notes,
        human_review_required=payload.human_review_required,
        prompt_items_json=json.dumps(payload.prompt_items, ensure_ascii=False),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "prompt_set.created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        metadata={"name": payload.name, "purpose": payload.purpose},
    )
    db.commit()
    db.refresh(row)
    return PromptSetRead(
        id=row.id,
        workspace_id=row.workspace_id,
        name=row.name,
        description=row.description,
        purpose=row.purpose,
        output_format=row.output_format,
        model_recommendation=row.model_recommendation,
        risk_notes=row.risk_notes,
        human_review_required=row.human_review_required,
        prompt_items=payload.prompt_items,
        created_at=row.created_at,
    )
