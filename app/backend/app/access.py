from __future__ import annotations

import json
import secrets
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import (
    AuditLog,
    Project,
    User,
    Workspace,
    WorkspaceInvite,
    WorkspaceMembership,
)

ROLE_LEVELS = {"viewer": 10, "editor": 20, "admin": 30, "owner": 40}


def normalize_role(role: str) -> str:
    value = role.strip().lower()
    if value not in ROLE_LEVELS:
        raise HTTPException(status_code=400, detail=f"Unsupported role: {role}")
    return value


def issue_invite_token() -> str:
    return secrets.token_urlsafe(24)


def get_workspace_membership(
    db: Session, workspace_id: int, current_user: User
) -> Optional[WorkspaceMembership]:
    return (
        db.query(WorkspaceMembership)
        .filter(
            WorkspaceMembership.workspace_id == workspace_id,
            WorkspaceMembership.user_id == current_user.id,
        )
        .first()
    )


def require_workspace_access(
    db: Session,
    workspace_id: int,
    current_user: User,
    minimum_role: str = "viewer",
) -> tuple[Workspace, WorkspaceMembership]:
    workspace = db.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    membership = get_workspace_membership(db, workspace_id, current_user)
    if not membership:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    if ROLE_LEVELS[membership.role] < ROLE_LEVELS[normalize_role(minimum_role)]:
        raise HTTPException(status_code=403, detail="Insufficient workspace role.")
    return workspace, membership


def require_project_access(
    db: Session,
    project_id: int,
    current_user: User,
    minimum_role: str = "viewer",
) -> tuple[Project, WorkspaceMembership]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    _, membership = require_workspace_access(
        db, project.workspace_id, current_user, minimum_role=minimum_role
    )
    return project, membership


def ensure_owner_membership(db: Session, workspace: Workspace) -> None:
    existing = (
        db.query(WorkspaceMembership)
        .filter(
            WorkspaceMembership.workspace_id == workspace.id,
            WorkspaceMembership.user_id == workspace.owner_user_id,
        )
        .first()
    )
    if existing:
        if existing.role != "owner":
            existing.role = "owner"
        return
    db.add(
        WorkspaceMembership(
            workspace_id=workspace.id, user_id=workspace.owner_user_id, role="owner"
        )
    )


def record_audit_log(
    db: Session,
    event_type: str,
    user_id: Optional[int] = None,
    workspace_id: Optional[int] = None,
    project_id: Optional[int] = None,
    metadata: Optional[dict] = None,
) -> None:
    db.add(
        AuditLog(
            event_type=event_type,
            user_id=user_id,
            workspace_id=workspace_id,
            project_id=project_id,
            metadata_json=json.dumps(metadata or {}, ensure_ascii=False),
        )
    )


def accept_invite(
    db: Session, invite: WorkspaceInvite, user: User
) -> WorkspaceMembership:
    if invite.revoked_at is not None or invite.status == "revoked":
        raise HTTPException(status_code=404, detail="Invite has been revoked.")
    if invite.expires_at is not None and invite.expires_at <= datetime.utcnow():
        raise HTTPException(status_code=410, detail="Invite has expired.")
    if invite.email.strip().lower() != user.email.strip().lower():
        raise HTTPException(
            status_code=403, detail="Invite email does not match the current user."
        )
    existing = (
        db.query(WorkspaceMembership)
        .filter(
            WorkspaceMembership.workspace_id == invite.workspace_id,
            WorkspaceMembership.user_id == user.id,
        )
        .first()
    )
    role = normalize_role(invite.role)
    if existing:
        if ROLE_LEVELS[role] > ROLE_LEVELS[existing.role]:
            existing.role = role
        membership = existing
    else:
        membership = WorkspaceMembership(
            workspace_id=invite.workspace_id,
            user_id=user.id,
            role=role,
            invited_by_user_id=invite.invited_by_user_id,
        )
        db.add(membership)
    invite.status = "accepted"
    invite.accepted_at = datetime.utcnow()
    return membership
