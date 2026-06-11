from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .api import (
    artifacts,
    audit_runs,
    auth,
    brand_facts,
    projects,
    prompt_sets,
    providers,
    reports,
    scheduled_checks,
    settings,
    sov,
    workspaces,
)
from .config import Settings, load_settings
from .database import Base, init_database
from .metrics import metrics_payload


def create_app(custom_settings: Optional[Settings] = None) -> FastAPI:
    settings_obj = custom_settings or load_settings()
    init_database(settings_obj)
    from .database import engine as initialized_engine

    if settings_obj.auto_create_schema:
        Base.metadata.create_all(bind=initialized_engine)
    app = FastAPI(title=settings_obj.app_name, version="2.1.0")
    app.state.settings = settings_obj
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings_obj.cors_origin_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok", "version": "2.1.0"}

    @app.get("/readyz")
    def readyz() -> dict:
        return {"status": "ready", "database": settings_obj.database_url}

    @app.get("/metrics")
    def metrics() -> Response:
        payload, content_type = metrics_payload()
        return Response(content=payload, media_type=content_type)

    app.include_router(auth.router, prefix=settings_obj.api_prefix)
    app.include_router(workspaces.router, prefix=settings_obj.api_prefix)
    app.include_router(projects.router, prefix=settings_obj.api_prefix)
    app.include_router(brand_facts.router, prefix=settings_obj.api_prefix)
    app.include_router(providers.router, prefix=settings_obj.api_prefix)
    app.include_router(prompt_sets.router, prefix=settings_obj.api_prefix)
    app.include_router(scheduled_checks.router, prefix=settings_obj.api_prefix)
    app.include_router(audit_runs.router, prefix=settings_obj.api_prefix)
    app.include_router(reports.router, prefix=settings_obj.api_prefix)
    app.include_router(artifacts.router, prefix=settings_obj.api_prefix)
    app.include_router(sov.router, prefix=settings_obj.api_prefix)
    app.include_router(settings.router, prefix=settings_obj.api_prefix)
    return app


app = create_app()
