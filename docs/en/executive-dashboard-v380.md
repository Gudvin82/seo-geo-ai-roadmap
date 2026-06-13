# Executive Dashboard v3.8.0

`v3.8.0` adds a fuller executive dashboard surface for project-level reporting.

Machine-readable source:

- `GET /api/v1/settings/executive-dashboard?project_id=...`

UI surface:

- `app/frontend/index.html` -> `Executive`

The dashboard rolls up:

- executive score
- health band
- top priorities
- connected integrations
- connected CMS connectors
- CI gating context
