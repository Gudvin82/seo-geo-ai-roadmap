# Executive Dashboard v3.8.0

`v3.8.0` добавляет более полноценную executive dashboard surface для
project-level reporting.

Machine-readable source:

- `GET /api/v1/settings/executive-dashboard?project_id=...`

UI surface:

- `app/frontend/index.html` -> `Executive`

Dashboard собирает:

- executive score
- health band
- top priorities
- connected integrations
- connected CMS connectors
- CI gating context
