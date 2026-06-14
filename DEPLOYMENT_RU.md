# Деплой

## Что поддерживает v2.1.0

`v2.1.0` — это turnkey self-hosted hardening релиз продуктового слоя.

Поддерживаемые сценарии:

- локальный backend с SQLite
- Docker Compose с PostgreSQL
- self-hosted foundation из frontend + backend + worker
- demo seed mode
- production-style migration flow

## Быстрый старт через Docker Compose

1. Скопируйте env-файл:

```bash
cp .env.example .env
```

1. Обязательно проверьте:

- `APP_SECRET_KEY`
- `OPENAI_API_KEY` и другие ключи провайдеров при необходимости
- `APP_CORS_ORIGINS`, если frontend будет на другом хосте
- `POSTGRES_PASSWORD`
- `APP_AUTO_CREATE_SCHEMA=false` для production-style migration discipline

1. Поднимите стек:

```bash
docker compose up --build
```

1. Откройте:

- frontend: `http://localhost:3000`
- backend API: `http://localhost:8000`
- health check: `http://localhost:8000/healthz`
- readiness check: `http://localhost:8000/readyz`
- metrics: `http://localhost:8000/metrics`
- API docs: `http://localhost:8000/docs`

## Demo mode

1. Поднимите стек:

```bash
make demo
```

1. Войдите с данными:

- `demo@example.com`
- `DemoPlatform123`

1. Откройте frontend и посмотрите seeded workspace, project, report и artifact data.

## Локальная разработка backend без Docker

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r app/backend/requirements.txt
uvicorn app.backend.app.main:app --reload
```

База по умолчанию:

- SQLite
- путь: `app/backend/data/discoverability.db`

## Migrations

Для явного обновления схемы используйте Alembic:

```bash
PYTHONPATH=app/backend ./.venv/bin/python -m alembic upgrade head
```

Shortcut:

```bash
make migrate
```

## Переменные окружения

Основные настройки приложения:

- `APP_SECRET_KEY`
- `APP_DATABASE_URL`
- `APP_ARTIFACT_ROOT`
- `APP_DEFAULT_REPORT_LANGUAGE`
- `APP_CORS_ORIGINS`
- `APP_TOKEN_TTL_MINUTES`
- `APP_LOGIN_ATTEMPT_WINDOW_SECONDS`
- `APP_LOGIN_ATTEMPT_LIMIT`
- `APP_AUTO_CREATE_SCHEMA`

Провайдеры:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `PERPLEXITY_API_KEY`

Docker / infra:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `BACKEND_PORT`
- `FRONTEND_PORT`

## Частые проблемы

### Frontend открывается, но API не отвечает

Проверьте:

- backend-контейнер запущен
- `APP_CORS_ORIGINS` содержит origin frontend
- во frontend указан правильный API base

### Комментарии провайдера пропускаются

Проверьте:

- в workspace создан provider config
- указано корректное имя модели
- задана нужная env-переменная с API ключом

### Нет артефактов после аудита

Проверьте:

- `APP_ARTIFACT_ROOT` доступен на запись
- backend может создавать директории
- выбранные script-based проверки завершились успешно

### Ошибки подключения к PostgreSQL

Проверьте:

- `APP_DATABASE_URL`
- готовность database service
- креды в `.env`

## Production mode notes

- ставьте `APP_AUTO_CREATE_SCHEMA=false`
- прогоняйте Alembic migrations до подачи трафика
- терминируйте HTTPS через reverse proxy или load balancer
- регулярно ротируйте secrets и provider keys
- делайте backup PostgreSQL и artifact storage

## Reverse proxy note

Для production ставьте стек за Nginx, Caddy, Traefik или аналогичный reverse proxy,
чтобы HTTPS, headers и routing были явными и проверяемыми.

## Backup note

Минимум нужно резервировать:

- PostgreSQL data
- `APP_ARTIFACT_ROOT`
- deployment secrets вне репозитория

## Связанные документы

- [ARCHITECTURE_RU.md](./ARCHITECTURE_RU.md)
- [OPEN_SOURCE_AND_SAAS_BOUNDARY_RU.md](./OPEN_SOURCE_AND_SAAS_BOUNDARY_RU.md)
- [SECURITY_CHECKLIST_RU.md](./SECURITY_CHECKLIST_RU.md)
- [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
- [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)
- [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)
