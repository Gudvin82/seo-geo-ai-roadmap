# API Overview

Main API groups in the product layer:

- auth
- workspaces
- projects
- project research context
- brand facts
- providers
- prompt sets
- scheduled checks
- audit runs
- reports
- artifacts
- settings
- sov
- integrations and provider sync
- authenticated read-only MCP tools (`POST /api/v1/mcp`)

Principles:

- predictable REST structure
- token-based access
- per-user workspace isolation
- reusable script-backed audit services
- bilingual reporting support

The API foundation lives in `app/backend/app/api/`.

Reference docs:

- [API reference EN](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/docs/en/api-reference.md)
- [API reference RU](https://github.com/Gudvin82/seo-geo-ai-roadmap/blob/main/docs/ru/api-reference.md)
