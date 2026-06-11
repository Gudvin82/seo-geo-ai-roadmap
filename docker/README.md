# Docker Assets

This folder documents the self-hosted container layer for the app foundation.

- `docker-compose.yml` is the main entrypoint
- backend uses FastAPI + Uvicorn
- frontend uses static assets served by Nginx
- PostgreSQL is the default durable database
- SQLite remains available for local non-Docker demos through `APP_DATABASE_URL`
