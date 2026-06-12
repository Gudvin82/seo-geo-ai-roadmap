from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import LlmsValidatorRequest, LlmsValidatorResponse
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
