from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Artifact, Project, User, Workspace
from ..schemas import ArtifactRead

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


def _project_for_user(db: Session, project_id: int, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    workspace = db.get(Workspace, project.workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.get("", response_model=list[ArtifactRead])
def list_artifacts(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[ArtifactRead]:
    _project_for_user(db, project_id, current_user)
    rows = db.query(Artifact).filter(Artifact.project_id == project_id).order_by(Artifact.id.desc()).all()
    return [
        ArtifactRead(
            id=row.id,
            audit_run_id=row.audit_run_id,
            project_id=row.project_id,
            artifact_type=row.artifact_type,
            format=row.format,
            file_path=row.file_path,
            metadata=json.loads(row.metadata_json),
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.get("/{artifact_id}/download")
def download_artifact(artifact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> FileResponse:
    artifact = db.get(Artifact, artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found.")
    _project_for_user(db, artifact.project_id, current_user)
    path = Path(artifact.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Artifact file not found.")
    return FileResponse(path, filename=path.name)
