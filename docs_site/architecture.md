# App Architecture

`v2.0.0` keeps the methodology repository intact and adds a SaaS-ready layer.

Architecture summary:

- methodology layer for humans
- script layer for CLI execution
- app layer for API and UI
- docs-site and workflows for distribution

Backend stack:

- FastAPI
- pydantic
- SQLAlchemy
- SQLite fallback
- PostgreSQL-ready Docker deployment

Frontend stack:

- static HTML
- CSS
- JavaScript
- Nginx delivery

See the full docs:

- [ARCHITECTURE.md](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/ARCHITECTURE.md)
- [ARCHITECTURE_RU.md](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/ARCHITECTURE_RU.md)
