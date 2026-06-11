from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import ProviderConfiguration, User
from ..schemas import ProviderConfigCreate, ProviderConfigRead

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=list[ProviderConfigRead])
def list_providers(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ProviderConfiguration]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    return (
        db.query(ProviderConfiguration)
        .filter(ProviderConfiguration.workspace_id == workspace_id)
        .all()
    )


@router.post("", response_model=ProviderConfigRead)
def create_provider(
    payload: ProviderConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProviderConfiguration:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="admin"
    )
    row = ProviderConfiguration(**payload.model_dump())
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "provider.config_changed",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        metadata={
            "provider_name": payload.provider_name,
            "label": payload.label,
            "base_url": payload.base_url,
        },
    )
    db.commit()
    db.refresh(row)
    return row
