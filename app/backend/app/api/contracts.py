from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from ..schemas import ContractCatalogRead
from ..services.contracts_catalog import contracts_catalog

router = APIRouter(prefix="/contracts", tags=["contracts"])


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@router.get("/catalog", response_model=ContractCatalogRead)
def get_contract_catalog() -> ContractCatalogRead:
    return ContractCatalogRead(contracts=contracts_catalog())


@router.get("/{contract_id}")
def get_contract(contract_id: str) -> dict:
    item = next((row for row in contracts_catalog() if row["id"] == contract_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Contract not found.")
    path = _repo_root() / item["path"]
    if not path.exists():
        raise HTTPException(status_code=404, detail="Contract file is missing.")
    return json.loads(path.read_text(encoding="utf-8"))
