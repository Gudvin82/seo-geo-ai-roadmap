from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Project, Site, User, Workspace
from ..schemas import ProjectCreate, ProjectRead, SiteCreate, SiteRead

router = APIRouter(prefix="/projects", tags=["projects"])


def _check_workspace(db: Session, workspace_id: int, current_user: User) -> Workspace:
    workspace = db.get(Workspace, workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return workspace


@router.get("", response_model=list[ProjectRead])
def list_projects(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Project]:
    _check_workspace(db, workspace_id, current_user)
    return db.query(Project).filter(Project.workspace_id == workspace_id).all()


@router.post("", response_model=ProjectRead)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    _check_workspace(db, payload.workspace_id, current_user)
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    _check_workspace(db, project.workspace_id, current_user)
    return project


@router.post("/{project_id}/sites", response_model=SiteRead)
def create_site(
    project_id: int,
    payload: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Site:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    _check_workspace(db, project.workspace_id, current_user)
    site = Site(
        project_id=project_id, canonical_url=payload.canonical_url, notes=payload.notes
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("/{project_id}/sites", response_model=list[SiteRead])
def list_sites(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Site]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    _check_workspace(db, project.workspace_id, current_user)
    return db.query(Site).filter(Site.project_id == project_id).all()
