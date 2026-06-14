from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.requests import Request

from .api import (
    agent_mode,
    artifacts,
    audit_logs,
    audit_runs,
    auth,
    brand_facts,
    cms,
    contracts,
    deliverables,
    exports,
    graph_runtime,
    integrations,
    notifications,
    projects,
    prompt_sets,
    providers,
    reports,
    scanner,
    scheduled_checks,
    settings,
    sov,
    task_center,
    telegram,
    tools,
    trusted_delivery,
    workspaces,
)
from .config import Settings, load_settings
from .database import Base, init_database
from .metrics import APP_ERRORS, REQUEST_LATENCY_SECONDS, metrics_payload
from .services.logging import log_event


def create_app(custom_settings: Optional[Settings] = None) -> FastAPI:
    settings_obj = custom_settings or load_settings()
    init_database(settings_obj)
    from .database import engine as initialized_engine

    if settings_obj.auto_create_schema:
        Base.metadata.create_all(bind=initialized_engine)
    app = FastAPI(title=settings_obj.app_name, version="4.5.0")
    app.state.settings = settings_obj
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings_obj.cors_origin_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def metrics_and_logging_middleware(request: Request, call_next):
        import time

        started_at = time.perf_counter()
        path = request.url.path
        try:
            response = await call_next(request)
        except Exception as exc:
            duration = time.perf_counter() - started_at
            APP_ERRORS.labels(kind=exc.__class__.__name__, path=path).inc()
            REQUEST_LATENCY_SECONDS.labels(
                method=request.method, path=path, status="500"
            ).observe(duration)
            log_event(
                "request.error",
                method=request.method,
                path=path,
                duration_seconds=round(duration, 3),
                error=exc.__class__.__name__,
            )
            raise
        duration = time.perf_counter() - started_at
        REQUEST_LATENCY_SECONDS.labels(
            method=request.method, path=path, status=str(response.status_code)
        ).observe(duration)
        log_event(
            "request.completed",
            method=request.method,
            path=path,
            status=response.status_code,
            duration_seconds=round(duration, 3),
        )
        return response

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok", "version": "4.5.0"}

    @app.get("/readyz")
    def readyz() -> dict:
        return {"status": "ready", "database": "ok"}

    @app.get("/metrics")
    def metrics() -> Response:
        payload, content_type = metrics_payload()
        return Response(content=payload, media_type=content_type)

    app.include_router(auth.router, prefix=settings_obj.api_prefix)
    app.include_router(workspaces.router, prefix=settings_obj.api_prefix)
    app.include_router(projects.router, prefix=settings_obj.api_prefix)
    app.include_router(brand_facts.router, prefix=settings_obj.api_prefix)
    app.include_router(integrations.router, prefix=settings_obj.api_prefix)
    app.include_router(cms.router, prefix=settings_obj.api_prefix)
    app.include_router(providers.router, prefix=settings_obj.api_prefix)
    app.include_router(prompt_sets.router, prefix=settings_obj.api_prefix)
    app.include_router(scheduled_checks.router, prefix=settings_obj.api_prefix)
    app.include_router(audit_runs.router, prefix=settings_obj.api_prefix)
    app.include_router(audit_logs.router, prefix=settings_obj.api_prefix)
    app.include_router(reports.router, prefix=settings_obj.api_prefix)
    app.include_router(scanner.router, prefix=settings_obj.api_prefix)
    app.include_router(scanner.jobs_router, prefix=settings_obj.api_prefix)
    app.include_router(artifacts.router, prefix=settings_obj.api_prefix)
    app.include_router(sov.router, prefix=settings_obj.api_prefix)
    app.include_router(notifications.router, prefix=settings_obj.api_prefix)
    app.include_router(trusted_delivery.router, prefix=settings_obj.api_prefix)
    app.include_router(deliverables.router, prefix=settings_obj.api_prefix)
    app.include_router(exports.router, prefix=settings_obj.api_prefix)
    app.include_router(settings.router, prefix=settings_obj.api_prefix)
    app.include_router(agent_mode.router, prefix=settings_obj.api_prefix)
    app.include_router(task_center.router, prefix=settings_obj.api_prefix)
    app.include_router(graph_runtime.router, prefix=settings_obj.api_prefix)
    app.include_router(contracts.router, prefix=settings_obj.api_prefix)
    app.include_router(tools.router, prefix=settings_obj.api_prefix)
    app.include_router(telegram.router, prefix=settings_obj.api_prefix)
    return app


app = create_app()
