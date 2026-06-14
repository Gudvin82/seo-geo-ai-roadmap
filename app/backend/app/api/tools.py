from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import (
    CommandCatalogResponse,
    CommandRouteRead,
    CommandRouterRequest,
    FactDriftItemRead,
    FactDriftRequest,
    FactDriftResponse,
    LlmsValidatorRequest,
    LlmsValidatorResponse,
)
from ..services.command_router import command_catalog, resolve_command_route
from ..services.fact_drift import FactSurface, detect_fact_drift
from ..services.llms_validator import validate_llms_text, validate_llms_url

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("/command-catalog", response_model=CommandCatalogResponse)
def get_command_catalog() -> CommandCatalogResponse:
    return CommandCatalogResponse(
        routes=[
            CommandRouteRead(
                command=item.command,
                title=item.title,
                summary=item.summary,
                intent=item.intent,
                aliases=item.aliases,
                recommended_scripts=item.recommended_scripts,
                recommended_docs=item.recommended_docs,
                api_routes=item.api_routes,
                example_invocations=item.example_invocations,
                output_artifacts=item.output_artifacts,
                use_cases=item.use_cases,
                next_step=item.next_step,
            )
            for item in command_catalog()
        ]
    )


@router.get("/command-contract")
def command_contract() -> dict:
    return {
        "contract_version": "v5.1.0",
        "canonical_prefix": "/geo",
        "canonical_sequence": [
            "/geo quick",
            "/geo audit",
            "/geo graph",
            "/geo report",
            "/geo compare",
            "/geo agent",
        ],
        "product_modes": [
            "repo_methodology",
            "app_control_panel",
            "scanner_intake",
        ],
        "ci_first_class": True,
        "routes": [
            {
                "command": item.command,
                "aliases": item.aliases,
                "intent": item.intent,
                "example_invocations": item.example_invocations,
                "output_artifacts": item.output_artifacts,
                "use_cases": item.use_cases,
                "recommended_scripts": item.recommended_scripts,
                "recommended_docs": item.recommended_docs,
                "api_routes": item.api_routes,
                "next_step": item.next_step,
            }
            for item in command_catalog()
        ],
        "integration_touchpoints": [
            "GET /api/v1/integrations/contracts",
            "GET /api/v1/cms/contracts",
            "GET /api/v1/settings/ci-gating",
            "GET /api/v1/settings/product-modes",
            "GET /api/v1/contracts/catalog",
            "GET /api/v1/agent-mode/contract",
            "GET /api/v1/tasks/audit-run/{audit_run_id}",
            "GET /api/v1/graph-runtime/audit-run/{audit_run_id}",
        ],
    }


@router.post("/command-router", response_model=CommandRouteRead)
def command_router(payload: CommandRouterRequest) -> CommandRouteRead:
    try:
        item = resolve_command_route(payload.command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CommandRouteRead(
        command=item.command,
        title=item.title,
        summary=item.summary,
        intent=item.intent,
        aliases=item.aliases,
        recommended_scripts=item.recommended_scripts,
        recommended_docs=item.recommended_docs,
        api_routes=item.api_routes,
        example_invocations=item.example_invocations,
        output_artifacts=item.output_artifacts,
        use_cases=item.use_cases,
        next_step=item.next_step,
    )


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
