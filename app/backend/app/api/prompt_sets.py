from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import PromptSet, User, Workspace
from ..schemas import PromptSetCreate, PromptSetRead

router = APIRouter(prefix="/prompt-sets", tags=["prompts"])


def _workspace_for_user(
    db: Session, workspace_id: int, current_user: User
) -> Workspace:
    workspace = db.get(Workspace, workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return workspace


@router.get("", response_model=list[PromptSetRead])
def list_prompt_sets(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PromptSetRead]:
    _workspace_for_user(db, workspace_id, current_user)
    rows = db.query(PromptSet).filter(PromptSet.workspace_id == workspace_id).all()
    return [
        PromptSetRead(
            id=row.id,
            workspace_id=row.workspace_id,
            name=row.name,
            description=row.description,
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
    _workspace_for_user(db, payload.workspace_id, current_user)
    row = PromptSet(
        workspace_id=payload.workspace_id,
        name=payload.name,
        description=payload.description,
        prompt_items_json=json.dumps(payload.prompt_items, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return PromptSetRead(
        id=row.id,
        workspace_id=row.workspace_id,
        name=row.name,
        description=row.description,
        prompt_items=payload.prompt_items,
        created_at=row.created_at,
    )
