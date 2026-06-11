# Architecture

## v2.1.0 layer model

`seo-geo-ai-roadmap` now has four clear layers:

1. Methodology layer
   - `docs/`, `checklists/`, `prompts/`, `templates/`, `examples/`
   - human-readable execution logic
2. Script layer
   - `scripts/`
   - reusable CLI utilities and validators
3. App layer
   - `app/backend/`, `app/frontend/`, `app/shared/`
   - SaaS-ready product foundation
4. Distribution layer
   - `docs_site/`, `mkdocs.yml`, `.github/workflows/`
   - public docs and CI/CD

The app layer does not replace the repository methodology. It orchestrates and
reuses it.

## Backend architecture

Stack:

- Python
- FastAPI
- pydantic
- SQLAlchemy
- SQLite fallback for local development
- PostgreSQL-ready deployment through Docker
- Alembic migrations for production-style schema management

Structure:

- `app/backend/app/api/` for REST endpoints
- `app/backend/app/services/` for audit execution and reporting
- `app/backend/app/providers/` for multi-provider AI abstraction
- `app/backend/app/models.py` for durable domain entities
- `app/backend/tests/` for backend and API validation
- `app/backend/app/seed.py` for demo seed data

## Frontend architecture

The initial frontend is intentionally simple:

- static HTML, CSS, and JavaScript
- no build pipeline required
- bilingual labels for EN/RU operation
- direct API integration with the FastAPI backend
- explicit self-hosted MVP workflow rather than a cloud-only dashboard

This keeps the product layer deployable in self-hosted environments without
frontend framework sprawl.

## Shared logic strategy

The repository already contains practical scripts under `scripts/`.

For `v2.0.0`, the migration strategy is:

- preserve existing CLI usage
- let backend services call the same scripts where direct reuse is practical
- keep future room in `app/shared/` for extracted shared modules and schemas

This supports:

- manual CLI usage
- repo-driven usage
- app/API usage

## Data model

The SaaS foundation includes:

- User
- Workspace
- Project
- Site
- Audit Run
- Report
- Provider Configuration
- Brand Facts Profile
- Prompt Set
- Artifact
- Scheduled Check

Key relationships:

- one user -> many workspaces
- one workspace -> many projects
- one project -> many audit runs
- one project -> many artifacts and reports
- one project -> one or more truth-center / brand-facts profiles

## Provider abstraction

The provider layer normalizes first support for:

- OpenAI
- Anthropic / Claude
- Gemini
- Perplexity

Goals:

- common interface for prompt execution
- provider-specific model configuration
- env-based or config-based credential routing
- normalized error handling
- capability-matrix-first documentation

## Reporting and evidence flow

Each audit run produces:

- status
- selected checks
- findings
- score
- artifacts
- structured reports in Markdown and JSON

Artifacts are persisted to the backend artifact root and exposed through the API.

## Deployment model

The supported foundation for `v2.0.0` is:

- frontend container
- backend container
- PostgreSQL container
- optional worker container
- optional one-command startup through `make up` and `make demo`

See:

- [DEPLOYMENT.md](./DEPLOYMENT.md)
- [OPEN_SOURCE_AND_SAAS_BOUNDARY.md](./OPEN_SOURCE_AND_SAAS_BOUNDARY.md)

## Future SaaS roadmap

Intentionally left out of `v2.0.0`:

- billing and payments
- enterprise SSO
- complex tenancy and permissions
- usage metering
- warehouse-grade analytics
- production SLA guarantees

The current release is a strong product foundation, not a bloated enterprise
surface.
