from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import (
    Artifact,
    BrandFactsProfile,
    Project,
    ProviderConfiguration,
    Report,
    SovRun,
    User,
)
from ..schemas import ProjectImportRead, ProjectImportRequest

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/project-package")
def export_project_package(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    reports = db.query(Report).filter(Report.project_id == project_id).all()
    artifacts = db.query(Artifact).filter(Artifact.project_id == project_id).all()
    facts = (
        db.query(BrandFactsProfile)
        .filter(BrandFactsProfile.project_id == project_id)
        .all()
    )
    providers = (
        db.query(ProviderConfiguration)
        .filter(ProviderConfiguration.workspace_id == project.workspace_id)
        .all()
    )
    sov_runs = db.query(SovRun).filter(SovRun.project_id == project_id).all()
    record_audit_log(
        db,
        "project.package_exported",
        user_id=current_user.id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        metadata={"report_count": len(reports), "artifact_count": len(artifacts)},
    )
    db.commit()
    return {
        "project": {
            "id": project.id,
            "workspace_id": project.workspace_id,
            "name": project.name,
            "website_url": project.website_url,
            "market": project.market,
            "language": project.language,
            "project_type": project.project_type,
            "audit_preset": project.audit_preset,
        },
        "reports": [
            {
                "id": row.id,
                "audit_run_id": row.audit_run_id,
                "language": row.language,
                "format": row.format,
                "summary_markdown": row.summary_markdown,
                "summary_json": json.loads(row.summary_json),
            }
            for row in reports
        ],
        "artifacts": [
            {
                "id": row.id,
                "artifact_type": row.artifact_type,
                "format": row.format,
                "file_path": row.file_path,
                "metadata": json.loads(row.metadata_json or "{}"),
            }
            for row in artifacts
        ],
        "brand_facts": [
            {
                "id": row.id,
                "name": row.name,
                "facts_markdown": row.facts_markdown,
                "approved_claims": row.approved_claims,
                "forbidden_claims": row.forbidden_claims,
                "numeric_facts": json.loads(row.numeric_facts_json or "[]"),
                "markets": json.loads(row.markets_json or "[]"),
                "languages": json.loads(row.languages_json or "[]"),
                "primary_cta": row.primary_cta,
            }
            for row in facts
        ],
        "provider_templates": [
            {
                "id": row.id,
                "provider_name": row.provider_name,
                "label": row.label,
                "model": row.model,
                "base_url": row.base_url,
                "api_key_env_var": row.api_key_env_var,
                "is_enabled": row.is_enabled,
            }
            for row in providers
        ],
        "sov_runs": [
            {
                "id": row.id,
                "brand": row.brand,
                "queries": json.loads(row.queries_json or "[]"),
                "providers": json.loads(row.providers_json or "[]"),
                "results": json.loads(row.results_json or "[]"),
                "mention_summary": row.mention_summary,
                "share_estimate": row.share_estimate,
            }
            for row in sov_runs
        ],
    }


@router.post("/project-package/import", response_model=ProjectImportRead)
def import_project_package(
    payload: ProjectImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectImportRead:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="editor"
    )
    project_payload = payload.payload.get("project") or {}
    project = Project(
        workspace_id=payload.workspace_id,
        name=project_payload.get("name", "Imported project"),
        website_url=project_payload.get("website_url", "https://example.com"),
        market=project_payload.get("market", "Global"),
        language=project_payload.get("language", "en"),
        project_type=project_payload.get("project_type", "imported_project"),
        audit_preset=project_payload.get("audit_preset", "global_multilingual"),
    )
    db.add(project)
    db.flush()
    for facts in payload.payload.get("brand_facts", []):
        db.add(
            BrandFactsProfile(
                project_id=project.id,
                name=facts.get("name", "Imported facts"),
                facts_markdown=facts.get("facts_markdown", ""),
                approved_claims=facts.get("approved_claims", ""),
                forbidden_claims=facts.get("forbidden_claims", ""),
                numeric_facts_json=json.dumps(
                    facts.get("numeric_facts", []), ensure_ascii=False
                ),
                markets_json=json.dumps(facts.get("markets", []), ensure_ascii=False),
                languages_json=json.dumps(
                    facts.get("languages", []), ensure_ascii=False
                ),
                primary_cta=facts.get("primary_cta"),
            )
        )
    record_audit_log(
        db,
        "project.package_imported",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=project.id,
        metadata={"imported_sections": list(payload.payload.keys())},
    )
    db.commit()
    return ProjectImportRead(
        project_id=project.id,
        imported_sections=list(payload.payload.keys()),
        message="Project package imported.",
    )
