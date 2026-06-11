from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..access import (
    accept_invite,
    ensure_owner_membership,
    issue_invite_token,
    normalize_role,
    record_audit_log,
    require_workspace_access,
)
from ..database import get_db
from ..deps import get_current_user
from ..metrics import INVITE_ACCEPTANCES, ROLE_CHANGES
from ..models import User, Workspace, WorkspaceInvite, WorkspaceMembership
from ..schemas import (
    WorkspaceCreate,
    WorkspaceInviteAccept,
    WorkspaceInviteCreate,
    WorkspaceInviteRead,
    WorkspaceMembershipRead,
    WorkspaceRead,
    WorkspaceUpdate,
)

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[WorkspaceRead])
def list_workspaces(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Workspace]:
    rows = (
        db.query(Workspace)
        .join(WorkspaceMembership, WorkspaceMembership.workspace_id == Workspace.id)
        .filter(WorkspaceMembership.user_id == current_user.id)
        .order_by(Workspace.id.asc())
        .all()
    )
    for workspace in rows:
        ensure_owner_membership(db, workspace)
    db.commit()
    return rows


@router.post("", response_model=WorkspaceRead)
def create_workspace(
    payload: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Workspace:
    workspace = Workspace(owner_user_id=current_user.id, **payload.model_dump())
    db.add(workspace)
    db.flush()
    ensure_owner_membership(db, workspace)
    record_audit_log(
        db,
        "workspace.created",
        user_id=current_user.id,
        workspace_id=workspace.id,
        metadata={"slug": workspace.slug},
    )
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("/{workspace_id}", response_model=WorkspaceRead)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Workspace:
    workspace, _ = require_workspace_access(db, workspace_id, current_user)
    return workspace


@router.put("/{workspace_id}", response_model=WorkspaceRead)
def update_workspace(
    workspace_id: int,
    payload: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Workspace:
    workspace, _ = require_workspace_access(
        db, workspace_id, current_user, minimum_role="editor"
    )
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(workspace, key, value)
    record_audit_log(
        db,
        "workspace.updated",
        user_id=current_user.id,
        workspace_id=workspace.id,
        metadata=payload.model_dump(exclude_none=True),
    )
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMembershipRead])
def list_memberships(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[WorkspaceMembership]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="viewer")
    return (
        db.query(WorkspaceMembership)
        .filter(WorkspaceMembership.workspace_id == workspace_id)
        .order_by(WorkspaceMembership.id.asc())
        .all()
    )


@router.post("/{workspace_id}/invites", response_model=WorkspaceInviteRead)
def create_invite(
    workspace_id: int,
    payload: WorkspaceInviteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceInvite:
    require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
    invite = WorkspaceInvite(
        workspace_id=workspace_id,
        email=payload.email,
        role=normalize_role(payload.role),
        invite_token=issue_invite_token(),
        invited_by_user_id=current_user.id,
    )
    db.add(invite)
    record_audit_log(
        db,
        "workspace.invite_created",
        user_id=current_user.id,
        workspace_id=workspace_id,
        metadata={"email": payload.email, "role": payload.role},
    )
    db.commit()
    db.refresh(invite)
    return invite


@router.get("/{workspace_id}/invites", response_model=list[WorkspaceInviteRead])
def list_invites(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[WorkspaceInvite]:
    require_workspace_access(db, workspace_id, current_user, minimum_role="admin")
    return (
        db.query(WorkspaceInvite)
        .filter(WorkspaceInvite.workspace_id == workspace_id)
        .order_by(WorkspaceInvite.id.desc())
        .all()
    )


@router.post("/invites/accept", response_model=WorkspaceMembershipRead)
def accept_workspace_invite(
    payload: WorkspaceInviteAccept,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceMembership:
    invite = (
        db.query(WorkspaceInvite)
        .filter(WorkspaceInvite.invite_token == payload.invite_token)
        .first()
    )
    if not invite or invite.status != "pending":
        raise HTTPException(status_code=404, detail="Invite not found or already used.")
    membership = accept_invite(db, invite, current_user)
    INVITE_ACCEPTANCES.labels(role=membership.role).inc()
    ROLE_CHANGES.labels(role=membership.role).inc()
    record_audit_log(
        db,
        "workspace.invite_accepted",
        user_id=current_user.id,
        workspace_id=invite.workspace_id,
        metadata={"role": membership.role, "invite_id": invite.id},
    )
    db.commit()
    db.refresh(membership)
    return membership
