# Deployment

## What v2.1.0 supports

`v2.1.0` is a turnkey self-hosted hardening release of the product layer.

Supported deployment paths:

- local backend with SQLite
- Docker Compose with PostgreSQL
- self-hosted frontend + backend + worker foundation
- demo seed mode
- production-style migration flow

## Quick start with Docker Compose

1. Copy environment defaults:

```bash
cp .env.example .env
```

1. Adjust at least:

- `APP_SECRET_KEY`
- `OPENAI_API_KEY` and other provider keys if needed
- `APP_CORS_ORIGINS` if frontend runs on another host
- `POSTGRES_PASSWORD`
- `APP_AUTO_CREATE_SCHEMA=false` for production-style migration discipline

1. Start the stack:

```bash
docker compose up --build
```

1. Open:

- frontend: `http://localhost:3000`
- backend API: `http://localhost:8000`
- health check: `http://localhost:8000/healthz`
- readiness check: `http://localhost:8000/readyz`
- metrics: `http://localhost:8000/metrics`
- API docs: `http://localhost:8000/docs`

## Demo mode

1. Start the stack:

```bash
make demo
```

1. Log in with:

- `demo@example.com`
- `DemoPlatform123`

1. Open the frontend and review seeded workspace, project, report, and artifact data.

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

## Migrations

Use Alembic for explicit schema upgrades:

```bash
PYTHONPATH=app/backend ./.venv/bin/python -m alembic upgrade head
```

Shortcut:

```bash
make migrate
```

## Environment variables

Core app:

- `APP_SECRET_KEY`
- `APP_DATABASE_URL`
- `APP_ARTIFACT_ROOT`
- `APP_DEFAULT_REPORT_LANGUAGE`
- `APP_CORS_ORIGINS`
- `APP_TOKEN_TTL_MINUTES`
- `APP_LOGIN_ATTEMPT_WINDOW_SECONDS`
- `APP_LOGIN_ATTEMPT_LIMIT`
- `APP_AUTO_CREATE_SCHEMA`

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

## Production mode notes

- set `APP_AUTO_CREATE_SCHEMA=false`
- run Alembic migrations before serving traffic
- terminate HTTPS at a reverse proxy or load balancer
- rotate secrets and provider keys on a schedule
- back up PostgreSQL data and artifact storage

## Reverse proxy note

For production, place the stack behind Nginx, Caddy, Traefik, or an equivalent
reverse proxy so HTTPS, headers, and routing stay explicit and auditable.

## Backup note

At minimum, back up:

- PostgreSQL data
- `APP_ARTIFACT_ROOT`
- deployment secrets outside the repository

## Docs and architecture

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [OPEN_SOURCE_AND_SAAS_BOUNDARY.md](./OPEN_SOURCE_AND_SAAS_BOUNDARY.md)
- [SECURITY_CHECKLIST.md](./SECURITY_CHECKLIST.md)
