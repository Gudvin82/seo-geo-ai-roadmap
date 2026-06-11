# Operations Runbook

## Базовые проверки

- API health: `GET /healthz`
- API readiness: `GET /readyz`
- Metrics: `GET /metrics`
- OpenAPI docs: `GET /docs`

## Типовые процедуры

### Перезапуск

- Docker: `docker compose restart backend frontend worker`
- Локальный backend: перезапустить `uvicorn`

### Миграции

- Применить: `make migrate`
- Проверить demo dataset: `make seed`

### Базовый backup

- dump базы данных
- `app/backend/artifacts` или смонтированный artifact volume
- `.env` и references на provider config

### Demo reset

- удалить dev-базу
- повторно выполнить `make migrate`
- повторно выполнить `make seed`

## Диагностика сбоев

- auth failures: смотреть `/api/v1/audit-logs?workspace_id=...`
- provider failures: смотреть `/metrics` и сгенерированные artifacts
- проблемы с reports: сначала смотреть artifact download output
- проблемы с migrations: проверить `APP_DATABASE_URL` и повторить Alembic

## Local tracing starter

OpenTelemetry и Jaeger по умолчанию не включены, но платформа готова к
дальнейшей легкой instrumentation без тяжелого enterprise-стека в v2.2.0.
