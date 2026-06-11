from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import BrandFactsProfile, Project, User, Workspace
from ..schemas import BrandFactsCreate, BrandFactsRead

router = APIRouter(prefix="/brand-facts", tags=["brand-facts"])


def _project_for_user(db: Session, project_id: int, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    workspace = db.get(Workspace, project.workspace_id)
    if not workspace or workspace.owner_user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.get("/{project_id}", response_model=list[BrandFactsRead])
def list_brand_facts(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[BrandFactsRead]:
    _project_for_user(db, project_id, current_user)
    rows = db.query(BrandFactsProfile).filter(BrandFactsProfile.project_id == project_id).all()
    return [
        BrandFactsRead(
            id=row.id,
            project_id=row.project_id,
            name=row.name,
            facts_markdown=row.facts_markdown,
            approved_claims=row.approved_claims,
            forbidden_claims=row.forbidden_claims,
            numeric_facts=json.loads(row.numeric_facts_json),
            markets=json.loads(row.markets_json),
            languages=json.loads(row.languages_json),
            primary_cta=row.primary_cta,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.post("", response_model=BrandFactsRead)
def create_brand_facts(
    payload: BrandFactsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BrandFactsRead:
    _project_for_user(db, payload.project_id, current_user)
    row = BrandFactsProfile(
        project_id=payload.project_id,
        name=payload.name,
        facts_markdown=payload.facts_markdown,
        approved_claims=payload.approved_claims,
        forbidden_claims=payload.forbidden_claims,
        numeric_facts_json=json.dumps(payload.numeric_facts, ensure_ascii=False),
        markets_json=json.dumps(payload.markets, ensure_ascii=False),
        languages_json=json.dumps(payload.languages, ensure_ascii=False),
        primary_cta=payload.primary_cta,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return BrandFactsRead(
        id=row.id,
        project_id=row.project_id,
        name=row.name,
        facts_markdown=row.facts_markdown,
        approved_claims=row.approved_claims,
        forbidden_claims=row.forbidden_claims,
        numeric_facts=payload.numeric_facts,
        markets=payload.markets,
        languages=payload.languages,
        primary_cta=row.primary_cta,
        created_at=row.created_at,
    )
