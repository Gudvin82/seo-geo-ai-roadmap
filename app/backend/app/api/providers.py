from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import ProviderConfiguration, User, Workspace
from ..schemas import ProviderConfigCreate, ProviderConfigRead

router = APIRouter(prefix="/providers", tags=["providers"])


def _workspace_for_user(db: Session, workspace_id: int, current_user: User) -> Workspace:
    workspace = db.get(Workspace, workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return workspace


@router.get("", response_model=list[ProviderConfigRead])
def list_providers(workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[ProviderConfiguration]:
    _workspace_for_user(db, workspace_id, current_user)
    return db.query(ProviderConfiguration).filter(ProviderConfiguration.workspace_id == workspace_id).all()


@router.post("", response_model=ProviderConfigRead)
def create_provider(
    payload: ProviderConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProviderConfiguration:
    _workspace_for_user(db, payload.workspace_id, current_user)
    row = ProviderConfiguration(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
