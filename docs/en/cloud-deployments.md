# Optional Cloud Deployment Notes

The platform is self-hosted first. Cloud examples are optional accelerators, not requirements.

## Railway

- Deploy the backend container.
- Provide PostgreSQL and set `APP_DATABASE_URL`.
- Set `APP_AUTO_CREATE_SCHEMA=false`.
- Run `alembic upgrade head` during release or startup scripting.

## Fly.io / Render style deployment

- Deploy frontend and backend as separate services if needed.
- Store provider keys and app secrets in platform secrets.
- Mount or externalize artifact storage if reports must persist.
