# Деплой

## Что поддерживает v2.0.0

`v2.0.0` — это первый self-hostable продуктовый слой репозитория.

Поддерживаемые сценарии:

- локальный backend с SQLite
- Docker Compose с PostgreSQL
- self-hosted foundation из frontend + backend + worker

## Быстрый старт через Docker Compose

1. Скопируйте env-файл:

```bash
cp .env.example .env
```

2. Обязательно проверьте:

- `APP_SECRET_KEY`
- `OPENAI_API_KEY` и другие ключи провайдеров при необходимости
- `APP_CORS_ORIGINS`, если frontend будет на другом хосте

3. Поднимите стек:

```bash
docker compose up --build
```

4. Откройте:

- frontend: `http://localhost:3000`
- backend API: `http://localhost:8000`
- health check: `http://localhost:8000/healthz`

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

## Переменные окружения

Основные настройки приложения:

- `APP_SECRET_KEY`
- `APP_DATABASE_URL`
- `APP_ARTIFACT_ROOT`
- `APP_DEFAULT_REPORT_LANGUAGE`
- `APP_CORS_ORIGINS`

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

## Связанные документы

- [ARCHITECTURE_RU.md](./ARCHITECTURE_RU.md)
- [OPEN_SOURCE_AND_SAAS_BOUNDARY_RU.md](./OPEN_SOURCE_AND_SAAS_BOUNDARY_RU.md)
