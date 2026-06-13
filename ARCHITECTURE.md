# Architecture

## Layer model in v3.5.0

`seo-geo-ai-roadmap` now has four practical layers:

1. Methodology layer
   - `docs/`, `checklists/`, `prompts/`, `templates/`, `examples/`
2. Script layer
   - `scripts/`
3. App layer
   - `app/backend/`, `app/frontend/`, `app/shared/`
4. Distribution layer
   - `docs_site/`, `mkdocs.yml`, `.github/workflows/`

For the public-facing architecture brief, see
[ARCHITECTURE_NOTE.md](./ARCHITECTURE_NOTE.md).

The app layer does not replace the methodology. It operationalizes it.

## Backend architecture

Core stack:

- Python
- FastAPI
- SQLAlchemy
- SQLite for local fallback
- PostgreSQL-ready Docker path

Key backend responsibilities:

- auth and workspace isolation
- provider configuration
- audit execution
- reporting and artifacts
- AI SoV persistence
- observability and structured logs

## Frontend architecture

The frontend stays intentionally lightweight:

- static HTML, CSS, and JavaScript
- no required build pipeline
- EN/RU operator labels
- direct API integration

This keeps the platform deployable in self-hosted environments without a heavy
frontend dependency tree.

## v3.5.0 additions on top of the core stack

- operator overview pane
- first-run guidance inside the app
- compact history charts
- clearer provider, audit, report, and SoV flow visibility
- AI handoff task packs for common deployment and audit tasks
- scanner-oriented bootstrap path for teams extending the audit core

## Shared logic strategy

The repository still values CLI usability. The platform is meant to complement
the scripts, not bury them.

## Honest boundaries

The current architecture is designed for pragmatic self-hosted operation. It is
not yet a full enterprise control plane with billing, SSO, or warehouse-grade
analytics.
