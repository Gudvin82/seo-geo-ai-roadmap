from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import GeneratedProjectManifest, User
from ..schemas import ProjectGenerationRead, ProjectGenerationRequest

router = APIRouter(prefix="/generation", tags=["generation"])


BLUEPRINT_SCHEMA_FILES = [
    "contracts/project-blueprint.schema.json",
    "contracts/integration-bundle.schema.json",
    "contracts/site-shell.schema.json",
    "contracts/admin-shell.schema.json",
    "contracts/scanner-config.schema.json",
    "contracts/dashboard-config.schema.json",
    "contracts/tenant-setup.schema.json",
    "contracts/operator-handoff.schema.json",
]


def _template_pack(payload: ProjectGenerationRequest) -> dict:
    mapping = {
        "local_business": "WordPress local business",
        "agency_client_workspace": "Agency multi-client workspace",
        "b2b_saas_company": "React SaaS",
        "content_media_site": "Content/media site",
        "ecommerce_store": "E-commerce with Merchant Center",
        "consultant_solo_workspace": "Consultant solo workspace",
    }
    return {
        "name": mapping[payload.project_type],
        "recommended_integrations": payload.required_integrations,
        "required_secrets": [
            f"{value.upper()}_TOKEN"
            for value in payload.required_integrations[:4]
            if value.isidentifier()
        ],
        "required_approvals": [
            "billing decision" if payload.target_mode == "saas_box" else "none",
            "domain and credential confirmation",
        ],
    }


def _serialize_manifest(row: GeneratedProjectManifest) -> ProjectGenerationRead:
    return ProjectGenerationRead(
        id=row.id,
        workspace_id=row.workspace_id,
        project_id=row.project_id,
        blueprint_type=row.blueprint_type,
        target_mode=row.target_mode,
        status=row.status,
        input_payload=json.loads(row.input_json or "{}"),
        manifest=json.loads(row.manifest_json or "{}"),
        created_at=row.created_at,
    )


@router.get("/contracts")
def generation_contracts() -> dict:
    return {
        "project_generation_contract_version": "v5.0.0",
        "schema_files": BLUEPRINT_SCHEMA_FILES,
        "project_types": [
            "local_business",
            "agency_client_workspace",
            "b2b_saas_company",
            "content_media_site",
            "ecommerce_store",
            "consultant_solo_workspace",
        ],
        "target_modes": ["self_hosted", "saas_box", "managed_deployment"],
        "required_outputs": [
            "generated blueprint JSON",
            "generated configuration files",
            "generated starter docs",
            "generated UI shell",
            "generated integration checklist",
            "generated operator handoff docs",
        ],
    }


@router.post("/manifests/generate", response_model=ProjectGenerationRead)
def generate_manifest(
    payload: ProjectGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectGenerationRead:
    manifest = {
        "input": payload.model_dump(),
        "surfaces": [
            "marketing/public site",
            "admin panel",
            "scanner intake",
            "project dashboard",
            "executive dashboard",
            "integration settings",
            "tasks/issues center",
            "graph/runtime views",
            "reporting views",
            "auth/onboarding shell",
        ],
        "integration_bundle": payload.required_integrations,
        "template_pack": _template_pack(payload),
        "operator_handoff": {
            "language_preference": payload.language_preference,
            "verified_vs_assumed_rule": True,
            "next_questions_policy": "ask only missing questions",
        },
    }
    row = GeneratedProjectManifest(
        workspace_id=payload.workspace_id,
        project_id=payload.project_id,
        blueprint_type=payload.project_type,
        target_mode=payload.target_mode,
        status="generated",
        input_json=json.dumps(payload.model_dump(), ensure_ascii=False),
        manifest_json=json.dumps(manifest, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _serialize_manifest(row)


@router.get("/manifests", response_model=list[ProjectGenerationRead])
def list_manifests(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[ProjectGenerationRead]:
    rows = db.query(GeneratedProjectManifest).order_by(
        GeneratedProjectManifest.id.desc()
    )
    return [_serialize_manifest(row) for row in rows.limit(20).all()]
