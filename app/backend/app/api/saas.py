from __future__ import annotations

import hashlib
import json
import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import ensure_owner_membership, record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Organization, TenantApiKey, TenantProfile, User
from ..schemas import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationWorkspaceSummaryRead,
    TenantApiKeyCreate,
    TenantApiKeyRead,
    TenantProfileCreate,
    TenantProfileRead,
    TenantProfileUpdate,
    WorkspaceCatalogRead,
)

router = APIRouter(prefix="/saas", tags=["saas"])


def _tenant_quota_alerts(row: Optional[TenantProfile]) -> list[dict]:
    if not row:
        return []
    quota = json.loads(row.quota_json or "{}")
    usage = json.loads(row.usage_json or "{}")
    alerts: list[dict] = []
    for key, limit in quota.items():
        if not isinstance(limit, (int, float)) or limit <= 0:
            continue
        used = usage.get(f"{key}_used")
        if not isinstance(used, (int, float)):
            continue
        ratio = round(float(used) / float(limit), 3)
        status = "healthy"
        if ratio >= 1:
            status = "exceeded"
        elif ratio >= 0.8:
            status = "watch"
        alerts.append(
            {
                "metric": key,
                "limit": limit,
                "used": used,
                "ratio": ratio,
                "status": status,
            }
        )
    return alerts


def _tenant_usage_health(row: Optional[TenantProfile]) -> dict:
    alerts = _tenant_quota_alerts(row)
    if not row:
        return {
            "status": "missing",
            "healthy_metrics": 0,
            "watch_metrics": 0,
            "exceeded_metrics": 0,
        }
    return {
        "status": (
            "exceeded"
            if any(item["status"] == "exceeded" for item in alerts)
            else "watch"
            if any(item["status"] == "watch" for item in alerts)
            else "healthy"
        ),
        "healthy_metrics": sum(1 for item in alerts if item["status"] == "healthy"),
        "watch_metrics": sum(1 for item in alerts if item["status"] == "watch"),
        "exceeded_metrics": sum(1 for item in alerts if item["status"] == "exceeded"),
    }


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
    row: TenantApiKey, plain_text_token: Optional[str] = None
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


@router.get("/workspace-catalog", response_model=WorkspaceCatalogRead)
def workspace_catalog(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> WorkspaceCatalogRead:
    from ..models import Workspace

    organizations = {
        row.id: row
        for row in db.query(Organization)
        .filter(Organization.owner_user_id == current_user.id)
        .all()
    }
    items: list[OrganizationWorkspaceSummaryRead] = []
    for workspace in (
        db.query(Workspace).filter(Workspace.owner_user_id == current_user.id).all()
    ):
        tenant = (
            db.query(TenantProfile)
            .filter(TenantProfile.workspace_id == workspace.id)
            .order_by(TenantProfile.id.desc())
            .first()
        )
        organization = organizations.get(tenant.organization_id) if tenant else None
        items.append(
            OrganizationWorkspaceSummaryRead(
                organization_id=organization.id if organization else None,
                organization_name=organization.name if organization else None,
                workspace_id=workspace.id,
                workspace_name=workspace.name,
                workspace_slug=workspace.slug,
                tenant_name=tenant.tenant_name if tenant else None,
                plan_code=tenant.plan_code if tenant else None,
                plan_status=tenant.plan_status if tenant else None,
                usage_summary=json.loads(tenant.usage_json or "{}") if tenant else {},
                quota_summary=json.loads(tenant.quota_json or "{}") if tenant else {},
            )
        )
    return WorkspaceCatalogRead(items=items)


@router.get("/organization-switcher")
def organization_switcher(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> dict:
    from ..models import Workspace

    organizations = (
        db.query(Organization)
        .filter(Organization.owner_user_id == current_user.id)
        .order_by(Organization.id.asc())
        .all()
    )
    workspaces = (
        db.query(Workspace)
        .filter(Workspace.owner_user_id == current_user.id)
        .order_by(Workspace.id.asc())
        .all()
    )
    tenant_rows = (
        db.query(TenantProfile)
        .filter(TenantProfile.workspace_id.in_([row.id for row in workspaces] or [0]))
        .order_by(TenantProfile.id.desc())
        .all()
    )
    latest_tenant_by_workspace: dict[int, TenantProfile] = {}
    for row in tenant_rows:
        latest_tenant_by_workspace.setdefault(row.workspace_id, row)

    workspace_items = []
    for workspace in workspaces:
        tenant = latest_tenant_by_workspace.get(workspace.id)
        workspace_items.append(
            {
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
                "workspace_slug": workspace.slug,
                "organization_id": tenant.organization_id if tenant else None,
                "tenant_name": tenant.tenant_name if tenant else None,
                "plan_code": tenant.plan_code if tenant else None,
                "plan_status": tenant.plan_status if tenant else None,
                "usage_health": _tenant_usage_health(tenant),
            }
        )

    org_items = []
    for organization in organizations:
        matching = [
            item
            for item in workspace_items
            if item["organization_id"] == organization.id
        ]
        org_items.append(
            {
                "organization_id": organization.id,
                "name": organization.name,
                "slug": organization.slug,
                "workspace_count": len(matching),
                "active_workspace_ids": [item["workspace_id"] for item in matching],
            }
        )
    suggested_workspace_id = (
        workspace_items[0]["workspace_id"] if workspace_items else None
    )
    suggested_organization_id = (
        next(
            (
                item["organization_id"]
                for item in workspace_items
                if item["organization_id"] is not None
            ),
            None,
        )
        if workspace_items
        else None
    )
    return {
        "organizations": org_items,
        "workspaces": workspace_items,
        "suggested_workspace_id": suggested_workspace_id,
        "suggested_organization_id": suggested_organization_id,
    }


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


@router.patch("/tenant-profiles/{tenant_profile_id}", response_model=TenantProfileRead)
def update_tenant_profile(
    tenant_profile_id: int,
    payload: TenantProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TenantProfileRead:
    row = db.get(TenantProfile, tenant_profile_id)
    if not row:
        raise HTTPException(status_code=404, detail="Tenant profile not found.")
    require_workspace_access(db, row.workspace_id, current_user, minimum_role="admin")
    updates = payload.model_dump(exclude_unset=True)
    if "tenant_name" in updates:
        row.tenant_name = updates["tenant_name"]
    if "plan_code" in updates:
        row.plan_code = updates["plan_code"]
    if "plan_status" in updates:
        row.plan_status = updates["plan_status"]
    if "quota" in updates:
        row.quota_json = json.dumps(updates["quota"], ensure_ascii=False)
    if "usage" in updates:
        row.usage_json = json.dumps(updates["usage"], ensure_ascii=False)
    if "onboarding_state" in updates:
        row.onboarding_state_json = json.dumps(
            updates["onboarding_state"], ensure_ascii=False
        )
    if "tenant_settings" in updates:
        row.tenant_settings_json = json.dumps(
            updates["tenant_settings"], ensure_ascii=False
        )
    record_audit_log(
        db,
        "tenant_profile.updated",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        metadata={
            "tenant_profile_id": row.id,
            "updated_fields": sorted(updates.keys()),
        },
    )
    db.add(row)
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
    quota_alerts = _tenant_quota_alerts(tenant)
    usage_health = _tenant_usage_health(tenant)
    onboarding_state = (
        json.loads(tenant.onboarding_state_json or "{}") if tenant else {}
    )
    settings_summary = json.loads(tenant.tenant_settings_json or "{}") if tenant else {}
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
        "quota_alerts": quota_alerts,
        "usage_health": usage_health,
        "onboarding_state": onboarding_state,
        "settings_summary": settings_summary,
        "api_keys_count": len(api_keys),
        "api_keys": [
            {
                "id": row.id,
                "label": row.label,
                "key_prefix": row.key_prefix,
                "is_enabled": row.is_enabled,
                "last_used_at": row.last_used_at.isoformat()
                if row.last_used_at
                else None,
            }
            for row in api_keys[:5]
        ],
        "roles_supported": [
            "owner",
            "admin",
            "operator",
            "analyst",
            "client_viewer",
        ],
        "deployment_modes": ["self_hosted", "managed_deployment", "saas_box"],
        "onboarding_checklist": [
            {
                "step": "tenant_profile",
                "status": "done" if tenant else "missing",
            },
            {
                "step": "api_keys",
                "status": "done" if api_keys else "missing",
            },
            {
                "step": "quota_policy",
                "status": "done"
                if tenant and json.loads(tenant.quota_json or "{}")
                else "missing",
            },
            {
                "step": "usage_visibility",
                "status": "done"
                if tenant and json.loads(tenant.usage_json or "{}")
                else "missing",
            },
        ],
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
