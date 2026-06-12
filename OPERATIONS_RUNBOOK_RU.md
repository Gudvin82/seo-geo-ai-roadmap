# Operations Runbook

## Core checks

- API health: `GET /healthz`
- API readiness: `GET /readyz`
- Metrics: `GET /metrics`
- OpenAPI docs: `GET /docs`

## Ключевые operational signals

- request latency через `REQUEST_LATENCY_SECONDS`
- provider latency через `PROVIDER_LATENCY_SECONDS`
- provider failures через `PROVIDER_FAILURES`
- app errors через `APP_ERRORS`
- audit duration через `AUDIT_DURATION_SECONDS`
- background retry count через `BACKGROUND_JOB_RETRIES`

## Common procedures

### Restart

- Docker: `docker compose restart backend frontend worker`
- Local backend: перезапустить `uvicorn`

### Migrations

- Apply: `make migrate`
- Seed demo data: `make seed`

### Backup basics

- database dump
- `app/backend/artifacts` или смонтированный artifact volume
- `.env` и ссылки на provider configs

### Demo reset

- удалить dev database
- заново выполнить `make migrate`
- заново выполнить `make seed`

## Failure diagnosis

- auth failures: смотреть `/api/v1/audit-logs?workspace_id=...`
- provider failures: смотреть `/metrics`, structured logs и generated artifacts
- report issues: смотреть artifact payloads и benchmark summary до rerun
- migration issues: проверить `APP_DATABASE_URL` и повторить Alembic
- retry-heavy operations: проверять audit status и `BACKGROUND_JOB_RETRIES`

## Logging stance

В `v3.0.0` добавлены structured application events для:

- request completion и request errors
- provider-backed AI SoV execution
- provider-backed audit execution
- audit completion
- role changes и provider changes

## Backup and restore workflow

1. снять snapshot базы
2. сохранить artifacts
3. сохранить `.env` и deployment config
4. восстановить базу
5. восстановить artifact paths
6. выполнить `make verify-demo` или project-specific smoke checks
