from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..access import record_audit_log, require_project_access
from ..database import get_db
from ..deps import get_current_user
from ..models import Artifact, User
from ..schemas import ArtifactRead

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get("", response_model=list[ArtifactRead])
def list_artifacts(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ArtifactRead]:
    require_project_access(db, project_id, current_user, minimum_role="viewer")
    rows = (
        db.query(Artifact)
        .filter(Artifact.project_id == project_id)
        .order_by(Artifact.id.desc())
        .all()
    )
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
def download_artifact(
    artifact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FileResponse:
    artifact = db.get(Artifact, artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found.")
    project, _ = require_project_access(
        db, artifact.project_id, current_user, minimum_role="viewer"
    )
    path = Path(artifact.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Artifact file not found.")
    record_audit_log(
        db,
        "artifact.downloaded",
        user_id=current_user.id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        metadata={"artifact_id": artifact.id, "artifact_type": artifact.artifact_type},
    )
    db.commit()
    return FileResponse(path, filename=path.name)
