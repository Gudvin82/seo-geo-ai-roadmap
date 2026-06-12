from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import (
    FactDriftItemRead,
    FactDriftRequest,
    FactDriftResponse,
    LlmsValidatorRequest,
    LlmsValidatorResponse,
)
from ..services.fact_drift import FactSurface, detect_fact_drift
from ..services.llms_validator import validate_llms_text, validate_llms_url

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/llms-validator", response_model=LlmsValidatorResponse)
def llms_validator(payload: LlmsValidatorRequest) -> LlmsValidatorResponse:
    if not payload.url and not payload.content:
        raise HTTPException(
            status_code=400, detail="Provide either llms.txt URL or llms.txt content."
        )
    result = (
        validate_llms_url(payload.url)
        if payload.url
        else validate_llms_text(payload.content or "", checked_source="inline")
    )
    return LlmsValidatorResponse(
        is_valid=result.is_valid,
        line_count=result.line_count,
        checked_source=result.checked_source,
        warnings=result.warnings,
        recommendations=result.recommendations,
        observed_facts=result.observed_facts,
    )


@router.post("/fact-drift", response_model=FactDriftResponse)
def fact_drift(payload: FactDriftRequest) -> FactDriftResponse:
    result = detect_fact_drift(
        [FactSurface(name=item.name, content=item.content) for item in payload.surfaces]
    )
    return FactDriftResponse(
        status=result.status,
        surface_count=result.surface_count,
        drift_items=[
            FactDriftItemRead(
                drift_type=item.drift_type,
                severity=item.severity,
                observed=item.observed,
                inferred_issue=item.inferred_issue,
                recommended_next_step=item.recommended_next_step,
            )
            for item in result.drift_items
        ],
        detected_types=result.detected_types,
        limitations=result.limitations,
    )
