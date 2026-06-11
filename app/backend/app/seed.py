from __future__ import annotations

import json
from pathlib import Path

from .access import ensure_owner_membership
from .config import Settings, load_settings
from .database import create_session, init_database
from .models import (
    Artifact,
    AuditRun,
    BrandFactsProfile,
    Project,
    Report,
    User,
    Workspace,
)
from .security import hash_password


def seed_demo_data(settings: Settings | None = None) -> dict[str, str | int]:
    settings_obj = settings or load_settings()
    init_database(settings_obj)
    from .database import Base
    from .database import engine as initialized_engine

    Base.metadata.create_all(bind=initialized_engine)
    db = create_session()
    try:
        existing_workspace = (
            db.query(Workspace).filter(Workspace.slug == "demo-agency").first()
        )
        if existing_workspace:
            existing_project = (
                db.query(Project)
                .filter(Project.workspace_id == existing_workspace.id)
                .first()
            )
            return {
                "workspace_id": existing_workspace.id,
                "project_id": existing_project.id if existing_project else 0,
                "workspace_slug": existing_workspace.slug,
                "message": "Demo data already exists.",
            }

        user = User(
            email="demo@example.com", password_hash=hash_password("DemoPlatform123")
        )
        db.add(user)
        db.flush()

        workspace = Workspace(
            owner_user_id=user.id,
            name="Demo Agency Workspace",
            slug="demo-agency",
            default_report_language="en",
            client_report_title="Demo Discoverability Report",
            client_report_subtitle="Transparent self-hosted example dataset",
        )
        db.add(workspace)
        db.flush()
        ensure_owner_membership(db, workspace)

        project = Project(
            workspace_id=workspace.id,
            name="Demo Self-Hosted Site",
            website_url="https://example.com",
            market="Global",
            language="en",
            project_type="product_service_site",
            audit_preset="global_multilingual",
        )
        db.add(project)
        db.flush()

        brand_facts = BrandFactsProfile(
            project_id=project.id,
            name="Demo Truth Center",
            facts_markdown="# Demo facts\nThe platform is free, transparent, and self-hosted first.",
            approved_claims="- Self-hosted\n- Transparent outputs\n- AI optional",
            forbidden_claims="- Mandatory cloud\n- Hidden scoring",
            numeric_facts_json=json.dumps(
                ["4 providers", "2 languages"], ensure_ascii=False
            ),
            markets_json=json.dumps(["Global", "RU"], ensure_ascii=False),
            languages_json=json.dumps(["en", "ru"], ensure_ascii=False),
            primary_cta="Run an audit and export the report.",
        )
        db.add(brand_facts)
        db.flush()

        audit_run = AuditRun(
            workspace_id=workspace.id,
            project_id=project.id,
            user_id=user.id,
            status="completed",
            report_language="en",
            selected_checks_json=json.dumps(
                ["robots_ai_bots", "llms_txt", "factual_consistency"],
                ensure_ascii=False,
            ),
            finding_groups_json=json.dumps(
                [
                    {
                        "title": "Transparent startup baseline",
                        "category": "self_hosted_readiness",
                        "severity": "low",
                        "summary": "Demo project is wired to show the complete open-source flow.",
                        "recommendation": "Review provider settings and run a fresh audit on your own domain.",
                    }
                ],
                ensure_ascii=False,
            ),
            summary_score=92.0,
        )
        db.add(audit_run)
        db.flush()

        report_payload = {
            "project_name": project.name,
            "summary_score": 92.0,
            "findings": json.loads(audit_run.finding_groups_json),
        }
        report = Report(
            audit_run_id=audit_run.id,
            project_id=project.id,
            language="en",
            format="markdown",
            summary_markdown=(
                "# Demo discoverability report\n\n"
                "- Product mode: self-hosted first\n"
                "- Transparency: enabled\n"
                "- Next step: connect a real site and rerun the audit\n"
            ),
            summary_json=json.dumps(report_payload, ensure_ascii=False),
        )
        db.add(report)
        db.flush()

        artifact_dir = Path(settings_obj.artifact_root) / "demo-seed"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifact_dir / "demo-report.md"
        artifact_path.write_text(report.summary_markdown, encoding="utf-8")
        artifact = Artifact(
            audit_run_id=audit_run.id,
            project_id=project.id,
            artifact_type="demo_report",
            format="markdown",
            file_path=str(artifact_path),
            metadata_json=json.dumps({"seed": True}, ensure_ascii=False),
        )
        db.add(artifact)
        db.commit()

        return {
            "workspace_id": workspace.id,
            "project_id": project.id,
            "workspace_slug": workspace.slug,
            "message": "Demo data created.",
        }
    finally:
        db.close()


def main() -> None:
    result = seed_demo_data()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
