from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import GeneratedProjectManifest, User
from ..schemas import (
    ProjectGenerationRead,
    ProjectGenerationRequest,
    ProjectGenerationScaffoldRead,
)

router = APIRouter(prefix="/generation", tags=["generation"])

GENERATED_ROOT = Path("generated_projects")


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
        "landing_page": "Deployable landing page",
        "scanner_saas": "Scanner SaaS box",
        "agency_workspace": "Agency workspace",
        "local_business_dashboard": "Local business dashboard",
        "ecommerce_ops": "E-commerce ops system",
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


def _slug_from_input(payload: ProjectGenerationRequest) -> str:
    raw = urlparse(payload.domain_or_url).netloc or payload.domain_or_url
    normalized = "".join(
        character.lower() if character.isalnum() else "-" for character in raw.strip()
    )
    return (
        "-".join(part for part in normalized.split("-") if part) or "generated-project"
    )


def _scaffold_files(
    payload: ProjectGenerationRequest, manifest_id: int
) -> dict[str, str]:
    app_name = _slug_from_input(payload)
    manifest = {
        "project_type": payload.project_type,
        "target_mode": payload.target_mode,
        "business_type": payload.business_type,
        "target_geography": payload.target_geography,
        "primary_stack": payload.primary_stack,
        "required_integrations": payload.required_integrations,
        "language_preference": payload.language_preference,
        "market_mode": payload.market_mode,
        "domain_or_url": payload.domain_or_url,
    }
    return {
        "README.md": "\n".join(
            [
                f"# {app_name}",
                "",
                "Generated with Discoverability OS AI-to-App mode.",
                "",
                "## Included surfaces",
                "",
                "- marketing/public site",
                "- admin/operator shell",
                "- scanner intake",
                "- executive dashboard",
                "- integration settings",
                "- proof timeline",
                "",
                "## Next steps",
                "",
                "1. Fill `.env.example`.",
                "2. Review `operator-handoff.json`.",
                "3. Connect integrations.",
                "4. Run the first audit and executive refresh.",
                "",
            ]
        ),
        "generated-manifest.json": json.dumps(
            {"manifest_id": manifest_id, "input": manifest},
            ensure_ascii=False,
            indent=2,
        ),
        "operator-handoff.json": json.dumps(
            {
                "prompt": "Deploy this generated project, connect the requested integrations, and return the first executive summary.",
                "required_integrations": payload.required_integrations,
                "deploy_mode": payload.target_mode,
                "language_preference": payload.language_preference,
                "operator_rules": [
                    "verify before claiming completion",
                    "keep EN and RU aligned",
                    "export evidence after the first audit",
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        ".env.example": "\n".join(
            [
                "APP_ENV=production",
                "APP_DATABASE_URL=postgresql://user:password@localhost:5432/discoverability",
                "OPENAI_API_KEY=",
                "GSC_SERVICE_ACCOUNT_JSON=",
                "GA4_SERVICE_ACCOUNT_JSON=",
                "GOOGLE_ADS_DEVELOPER_TOKEN=",
                "YANDEX_WEBMASTER_TOKEN=",
                "YANDEX_METRICA_TOKEN=",
                "YANDEX_DIRECT_TOKEN=",
            ]
        )
        + "\n",
        "app-shell.json": json.dumps(
            {
                "site": {
                    "url": payload.domain_or_url,
                    "business_type": payload.business_type,
                },
                "surfaces": [
                    "overview",
                    "executive",
                    "scanner",
                    "saas",
                    "proof",
                    "generation",
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "deploy-wizard.json": json.dumps(
            {
                "preferred_path": payload.target_mode,
                "available_paths": [
                    "local",
                    "vps_docker",
                    "coolify",
                    "railway",
                    "render",
                    "kubernetes",
                ],
                "verification": [
                    "login",
                    "first audit",
                    "integration sync",
                    "proof export",
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "prompt-pack.md": "\n".join(
            [
                "# One-click prompt pack",
                "",
                "## Deploy for me",
                "",
                "Use this generated project and deploy it under the chosen runtime path.",
                "",
                "## Audit my site",
                "",
                "Run the scanner, the audit flow, proof export, and executive summary.",
                "",
                "## Generate client scanner",
                "",
                "Turn this project into a gated client scanner with operator review.",
                "",
            ]
        ),
    }


@router.get("/contracts")
def generation_contracts() -> dict:
    return {
        "project_generation_contract_version": "v6.7.0",
        "schema_files": BLUEPRINT_SCHEMA_FILES,
        "project_types": [
            "landing_page",
            "scanner_saas",
            "agency_workspace",
            "local_business_dashboard",
            "ecommerce_ops",
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


@router.post(
    "/manifests/{manifest_id}/scaffold", response_model=ProjectGenerationScaffoldRead
)
def scaffold_manifest(
    manifest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectGenerationScaffoldRead:
    row = db.get(GeneratedProjectManifest, manifest_id)
    if not row:
        raise HTTPException(status_code=404, detail="Manifest not found.")
    payload = ProjectGenerationRequest(**json.loads(row.input_json or "{}"))
    slug = _slug_from_input(payload)
    output_dir = GENERATED_ROOT / f"{slug}-{manifest_id}"
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files: list[str] = []
    for relative_path, content in _scaffold_files(payload, manifest_id).items():
        target = output_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        generated_files.append(str(target))
    manifest = json.loads(row.manifest_json or "{}")
    manifest["scaffold"] = {
        "output_directory": str(output_dir),
        "generated_files": generated_files,
    }
    row.status = "scaffolded"
    row.manifest_json = json.dumps(manifest, ensure_ascii=False)
    db.add(row)
    db.commit()
    return ProjectGenerationScaffoldRead(
        manifest_id=row.id,
        output_directory=str(output_dir),
        generated_files=generated_files,
        starter_urls={
            "overview": "/",
            "scanner": "/scanner.html",
            "graph": "/graph.html",
        },
        next_steps=[
            "fill the generated env example",
            "review operator-handoff.json",
            "connect requested integrations",
            "run first audit and proof capture",
        ],
    )
