# Deployment

## What v2.0.0 supports

`v2.0.0` is the first self-hostable product layer of the repository.

Supported deployment paths:

- local backend with SQLite
- Docker Compose with PostgreSQL
- self-hosted frontend + backend + worker foundation

## Quick start with Docker Compose

1. Copy environment defaults:

```bash
cp .env.example .env
```

2. Adjust at least:

- `APP_SECRET_KEY`
- `OPENAI_API_KEY` and other provider keys if needed
- `APP_CORS_ORIGINS` if frontend runs on another host

3. Start the stack:

```bash
docker compose up --build
```

4. Open:

- frontend: `http://localhost:3000`
- backend API: `http://localhost:8000`
- health check: `http://localhost:8000/healthz`

## Local backend-only development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r app/backend/requirements.txt
uvicorn app.backend.app.main:app --reload
```

Default local database:

- SQLite
- path: `app/backend/data/discoverability.db`

## Environment variables

Core app:

- `APP_SECRET_KEY`
- `APP_DATABASE_URL`
- `APP_ARTIFACT_ROOT`
- `APP_DEFAULT_REPORT_LANGUAGE`
- `APP_CORS_ORIGINS`

Providers:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `PERPLEXITY_API_KEY`

Docker / infrastructure:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `BACKEND_PORT`
- `FRONTEND_PORT`

## Common failure cases

### Frontend can load but API calls fail

Check:

- backend container is running
- `APP_CORS_ORIGINS` includes the frontend origin
- frontend API base points to the correct backend URL

### Provider commentary is skipped

Check:

- provider config exists in the workspace
- model name is valid
- matching API key env var is set

### Audit artifacts are missing

Check:

- `APP_ARTIFACT_ROOT` is writable
- backend has permission to create directories
- the selected script-based checks completed successfully

### PostgreSQL connection errors

Check:

- `APP_DATABASE_URL`
- database service readiness
- credentials in `.env`

## Docs and architecture

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [OPEN_SOURCE_AND_SAAS_BOUNDARY.md](./OPEN_SOURCE_AND_SAAS_BOUNDARY.md)
