# Проверка развёртывания

Этот релиз проверяется как self-hosted операторский сценарий, а не только как
набор документации.

## Fresh-path проверка

1. Клонируйте репозиторий и создайте `.env` из `.env.example`.
1. Установите backend-зависимости через `make install-backend`.
1. Примените схему через `make migrate`.
1. Загрузите demo-данные через `make seed`.
1. Поднимите стек через `make up` или используйте `./run-local.sh`.
1. Откройте:
   - `http://localhost:8000/healthz`
   - `http://localhost:8000/readyz`
   - `http://localhost:8000/docs`
   - `http://localhost:3000`
1. Войдите под:
   - `demo@example.com`
   - `DemoPlatform123`
1. Откройте seed-воркспейс и проект.
1. Запустите `POST /api/v1/audit-runs/run` или стартуйте аудит из UI.
1. Проверьте, что доступны reports и artifacts.

## Ожидаемые результаты

- `healthz` возвращает `status: ok`
- `readyz` возвращает `status: ready`
- `/docs` открывается
- demo-login возвращает bearer token с expiry metadata
- список workspaces не пуст
- список projects не пуст
- audit run возвращает `audit_job_id` и `initial_status`
- endpoint reports возвращает минимум один seed или generated report
- endpoint artifacts возвращает минимум один seed или generated artifact

## Автоматическая проверка

Запустите:

```bash
make verify-demo
```

Команда проверяет health, readiness, доступность docs, demo auth, минимальный
audit path и наличие reports и artifacts.
