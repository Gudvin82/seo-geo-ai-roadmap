from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import ProviderConfiguration, User
from ..providers.registry import (
    PROVIDERS,
    list_provider_catalog,
    model_registry_profiles,
    provider_catalog_entry,
    provider_catalog_summary,
    provider_runtime_kind,
)
from ..schemas import ProviderConfigCreate, ProviderConfigRead, ProviderConfigUpdate

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


@router.get("/catalog")
def provider_catalog() -> dict:
    return {
        "summary": provider_catalog_summary(),
        "providers": list_provider_catalog(),
    }


@router.get("/model-registry")
def provider_model_registry() -> dict:
    return {
        "summary": provider_catalog_summary(),
        "catalog": list_provider_catalog(),
        "registry_profiles": model_registry_profiles(),
    }


@router.get("/health")
def provider_health(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    rows = (
        db.query(ProviderConfiguration)
        .filter(ProviderConfiguration.workspace_id == workspace_id)
        .order_by(ProviderConfiguration.id.desc())
        .all()
    )
    items: list[dict] = []
    for row in rows:
        metadata = provider_catalog_entry(row.provider_name)
        env_var_name = row.api_key_env_var or ""
        env_present = bool(env_var_name and os.getenv(env_var_name))
        if metadata["auth_mode"] == "optional_or_none":
            credential_status = "not_required"
        elif env_var_name and env_present:
            credential_status = "env_resolved"
        elif env_var_name:
            credential_status = "env_declared_not_loaded"
        else:
            credential_status = "env_not_declared"
        readiness_score = 0
        if row.is_enabled:
            readiness_score += 35
        if row.model:
            readiness_score += 25
        if credential_status in {"not_required", "env_resolved"}:
            readiness_score += 25
        if row.base_url or metadata["default_endpoint"]:
            readiness_score += 15
        items.append(
            {
                "provider_id": row.id,
                "label": row.label,
                "provider_name": row.provider_name,
                "model": row.model,
                "is_enabled": row.is_enabled,
                "runtime_kind": provider_runtime_kind(row.provider_name),
                "credential_status": credential_status,
                "endpoint_mode": "custom_base_url"
                if row.base_url
                else "default_endpoint",
                "routing_role": metadata["routing_role"],
                "readiness_score": readiness_score,
                "recommended_next_step": (
                    "load the declared env var into the runtime"
                    if credential_status == "env_declared_not_loaded"
                    else "declare the provider env var and validate one live run"
                    if credential_status == "env_not_declared"
                    else "keep this provider as a healthy lane in the routing stack"
                ),
            }
        )
    healthy = [item for item in items if item["readiness_score"] >= 75]
    return {
        "workspace_id": workspace_id,
        "summary": {
            "configured": len(items),
            "healthy_or_ready": len(healthy),
            "supported_total": len(PROVIDERS),
            "hosted_supported": provider_catalog_summary()["hosted_supported"],
            "local_supported": provider_catalog_summary()["local_supported"],
        },
        "providers": items,
        "routing_advice": [
            "keep one frontier provider for strategic tasks",
            "keep one faster or cheaper provider for repeat jobs",
            "keep one local runtime for fallback and privacy-sensitive work",
        ],
    }


@router.get("/operating-center")
def provider_operating_center(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    health = provider_health(workspace_id, db, current_user)
    return {
        "workspace_id": workspace_id,
        "catalog_summary": provider_catalog_summary(),
        "health_summary": health["summary"],
        "providers": health["providers"],
        "registry_profiles": model_registry_profiles()["profiles"],
        "routing_policies": model_registry_profiles()["routing_policies"],
        "announcable_claim": (
            "multi-model platform with cloud and local runtime lanes"
            if health["summary"]["configured"] >= 2
            else "multi-model-ready platform with a wide provider surface"
        ),
    }


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


@router.put("/{provider_id}", response_model=ProviderConfigRead)
def update_provider(
    provider_id: int,
    payload: ProviderConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProviderConfiguration:
    row = db.get(ProviderConfiguration, provider_id)
    if not row:
        raise HTTPException(status_code=404, detail="Provider configuration not found.")
    require_workspace_access(db, row.workspace_id, current_user, minimum_role="admin")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(row, key, value)
    record_audit_log(
        db,
        "provider.config_changed",
        user_id=current_user.id,
        workspace_id=row.workspace_id,
        metadata={
            "provider_id": row.id,
            "provider_name": row.provider_name,
            "label": row.label,
            "is_enabled": row.is_enabled,
        },
    )
    db.commit()
    db.refresh(row)
    return row
