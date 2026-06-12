# Operations Runbook

## Core checks

- API health: `GET /healthz`
- API readiness: `GET /readyz`
- Metrics: `GET /metrics`
- OpenAPI docs: `GET /docs`

## Key operational signals

- request latency via `REQUEST_LATENCY_SECONDS`
- provider latency via `PROVIDER_LATENCY_SECONDS`
- provider failures via `PROVIDER_FAILURES`
- app errors via `APP_ERRORS`
- audit duration via `AUDIT_DURATION_SECONDS`
- background retry count via `BACKGROUND_JOB_RETRIES`

## Common procedures

### Restart

- Docker: `docker compose restart backend frontend worker`
- Local backend: restart `uvicorn`

### Migrations

- Apply: `make migrate`
- Seed demo data: `make seed`

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
- provider failures: inspect `/metrics`, structured logs, and generated
  artifacts
- report issues: inspect artifact payloads and benchmark summary before reruns
- migration issues: confirm `APP_DATABASE_URL` and rerun Alembic
- retry-heavy operations: inspect audit status and `BACKGROUND_JOB_RETRIES`

## Logging stance

`v3.0.0` adds structured application events for:

- request completion and request errors
- provider-backed AI SoV execution
- provider-backed audit execution
- audit completion
- role changes and provider changes

## Backup and restore workflow

1. snapshot the database
2. preserve artifacts
3. preserve `.env` and deployment config
4. restore database
5. restore artifact paths
6. run `make verify-demo` or project-specific smoke checks
