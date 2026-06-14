from __future__ import annotations

import hashlib
import json
import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import ensure_owner_membership, record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Organization, TenantApiKey, TenantProfile, User
from ..schemas import (
    OrganizationCreate,
    OrganizationRead,
    TenantApiKeyCreate,
    TenantApiKeyRead,
    TenantProfileCreate,
    TenantProfileRead,
)

router = APIRouter(prefix="/saas", tags=["saas"])


def _serialize_tenant_profile(row: TenantProfile) -> TenantProfileRead:
    return TenantProfileRead(
        id=row.id,
        workspace_id=row.workspace_id,
        organization_id=row.organization_id,
        tenant_name=row.tenant_name,
        plan_code=row.plan_code,
        plan_status=row.plan_status,
        quota=json.loads(row.quota_json or "{}"),
        usage=json.loads(row.usage_json or "{}"),
        onboarding_state=json.loads(row.onboarding_state_json or "{}"),
        tenant_settings=json.loads(row.tenant_settings_json or "{}"),
        created_at=row.created_at,
    )


def _serialize_api_key(
    row: TenantApiKey, plain_text_token: str | None = None
) -> TenantApiKeyRead:
    return TenantApiKeyRead(
        id=row.id,
        workspace_id=row.workspace_id,
        label=row.label,
        key_prefix=row.key_prefix,
        scopes=json.loads(row.scopes_json or "[]"),
        is_enabled=row.is_enabled,
        last_used_at=row.last_used_at,
        created_at=row.created_at,
        plain_text_token=plain_text_token,
    )


@router.get("/organizations", response_model=list[OrganizationRead])
def list_organizations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Organization]:
    return (
        db.query(Organization)
        .filter(Organization.owner_user_id == current_user.id)
        .order_by(Organization.id.asc())
        .all()
    )


@router.post("/organizations", response_model=OrganizationRead)
def create_organization(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:
    row = Organization(
        owner_user_id=current_user.id, name=payload.name, slug=payload.slug
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "organization.created",
        user_id=current_user.id,
        metadata={"organization_id": row.id, "slug": row.slug},
    )
    db.commit()
    db.refresh(row)
    return row


@router.get("/tenant-profiles", response_model=list[TenantProfileRead])
def list_tenant_profiles(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TenantProfileRead]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    rows = (
        db.query(TenantProfile)
        .filter(TenantProfile.workspace_id == workspace_id)
        .order_by(TenantProfile.id.desc())
        .all()
    )
    return [_serialize_tenant_profile(row) for row in rows]


@router.post("/tenant-profiles", response_model=TenantProfileRead)
def create_tenant_profile(
    payload: TenantProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TenantProfileRead:
    workspace, _ = require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="admin"
    )
    ensure_owner_membership(db, workspace)
    row = TenantProfile(
        workspace_id=payload.workspace_id,
        organization_id=payload.organization_id,
        tenant_name=payload.tenant_name,
        plan_code=payload.plan_code,
        plan_status=payload.plan_status,
        quota_json=json.dumps(payload.quota, ensure_ascii=False),
        usage_json=json.dumps(payload.usage, ensure_ascii=False),
        onboarding_state_json=json.dumps(payload.onboarding_state, ensure_ascii=False),
        tenant_settings_json=json.dumps(payload.tenant_settings, ensure_ascii=False),
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "tenant_profile.created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        metadata={"tenant_name": row.tenant_name, "plan_code": row.plan_code},
    )
    db.commit()
    db.refresh(row)
    return _serialize_tenant_profile(row)


@router.get("/tenant-overview")
def tenant_overview(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    workspace, membership = require_workspace_access(
        db, workspace_id, current_user, minimum_role="viewer"
    )
    tenant = (
        db.query(TenantProfile)
        .filter(TenantProfile.workspace_id == workspace_id)
        .order_by(TenantProfile.id.desc())
        .first()
    )
    api_keys = (
        db.query(TenantApiKey)
        .filter(TenantApiKey.workspace_id == workspace_id)
        .order_by(TenantApiKey.id.desc())
        .all()
    )
    return {
        "workspace_id": workspace.id,
        "workspace_slug": workspace.slug,
        "role": membership.role,
        "saas_mode": tenant is not None,
        "tenant_profile": _serialize_tenant_profile(tenant).model_dump()
        if tenant
        else None,
        "usage_summary": json.loads(tenant.usage_json or "{}") if tenant else {},
        "quota_summary": json.loads(tenant.quota_json or "{}") if tenant else {},
        "api_keys_count": len(api_keys),
        "roles_supported": [
            "owner",
            "admin",
            "operator",
            "analyst",
            "client_viewer",
        ],
        "deployment_modes": ["self_hosted", "managed_deployment", "saas_box"],
    }


@router.get("/api-keys", response_model=list[TenantApiKeyRead])
def list_api_keys(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TenantApiKeyRead]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
    rows = (
        db.query(TenantApiKey)
        .filter(TenantApiKey.workspace_id == workspace_id)
        .order_by(TenantApiKey.id.desc())
        .all()
    )
    return [_serialize_api_key(row) for row in rows]


@router.post("/api-keys", response_model=TenantApiKeyRead)
def create_api_key(
    payload: TenantApiKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TenantApiKeyRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="admin"
    )
    token = f"sgai_{secrets.token_urlsafe(24)}"
    row = TenantApiKey(
        workspace_id=payload.workspace_id,
        label=payload.label,
        key_prefix=token[:12],
        token_hash=hashlib.sha256(token.encode("utf-8")).hexdigest(),
        scopes_json=json.dumps(payload.scopes, ensure_ascii=False),
        is_enabled=True,
    )
    db.add(row)
    db.flush()
    record_audit_log(
        db,
        "tenant_api_key.created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        metadata={"label": row.label, "key_prefix": row.key_prefix},
    )
    db.commit()
    db.refresh(row)
    return _serialize_api_key(row, plain_text_token=token)
