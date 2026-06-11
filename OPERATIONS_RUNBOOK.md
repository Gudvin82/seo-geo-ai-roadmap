# Operations Runbook

## Core checks

- API health: `GET /healthz`
- API readiness: `GET /readyz`
- Metrics: `GET /metrics`
- OpenAPI docs: `GET /docs`

## Common procedures

### Restart

- Docker: `docker compose restart backend frontend worker`
- Local backend: restart `uvicorn`

### Migrations

- Apply: `make migrate`
- Verify demo dataset: `make seed`

### Backup basics

- database dump
- `app/backend/artifacts` or mounted artifact volume
- `.env` and provider config references

### Demo reset

- remove the dev database
- rerun `make migrate`
- rerun `make seed`

## Failure diagnosis

- auth failures: inspect `/api/v1/audit-logs?workspace_id=...`
- provider failures: inspect `/metrics` and generated artifacts
- report issues: inspect artifact download output before re-running
- migration issues: confirm `APP_DATABASE_URL` and rerun Alembic

## Local tracing starter

OpenTelemetry and Jaeger are not wired by default, but the platform is ready for
lightweight future instrumentation without requiring a heavy stack in v2.2.0.
