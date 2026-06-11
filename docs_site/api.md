# API Overview

Main API groups in the product layer:

- auth
- workspaces
- projects
- brand facts
- providers
- prompt sets
- scheduled checks
- audit runs
- reports
- artifacts
- settings

Principles:

- predictable REST structure
- token-based access
- per-user workspace isolation
- reusable script-backed audit services
- bilingual reporting support

The API foundation lives in `app/backend/app/api/`.
