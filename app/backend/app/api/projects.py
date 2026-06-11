from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access, require_workspace_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Project, Site, User
from ..schemas import ProjectCreate, ProjectRead, SiteCreate, SiteRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
def list_projects(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Project]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    return db.query(Project).filter(Project.workspace_id == workspace_id).all()


@router.post("", response_model=ProjectRead)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    require_workspace_access(
        db, payload.workspace_id, current_user, minimum_role="editor"
    )
    project = Project(**payload.model_dump())
    db.add(project)
    db.flush()
    record_audit_log(
        db,
        "project.created",
        user_id=current_user.id,
        workspace_id=payload.workspace_id,
        project_id=project.id,
        metadata={"website_url": payload.website_url, "name": payload.name},
    )
    db.commit()
    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    return project


@router.post("/{project_id}/sites", response_model=SiteRead)
def create_site(
    project_id: int,
    payload: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Site:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="editor"
    )
    site = Site(
        project_id=project_id, canonical_url=payload.canonical_url, notes=payload.notes
    )
    db.add(site)
    record_audit_log(
        db,
        "project.site_created",
        user_id=current_user.id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        metadata={"canonical_url": payload.canonical_url},
    )
    db.commit()
    db.refresh(site)
    return site


@router.get("/{project_id}/sites", response_model=list[SiteRead])
def list_sites(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Site]:
    project, _ = require_project_access(
        db, project_id, current_user, minimum_role="viewer"
    )
    return db.query(Site).filter(Site.project_id == project_id).all()
