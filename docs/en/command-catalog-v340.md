# Command Catalog

`v3.4.0` adds a command surface so humans and AI agents can map broad GEO tasks
to the right scripts, docs, and API routes without guessing.

## Core commands

- `audit`: full GEO and SEO audit flow
- `quick`: fast starter snapshot
- `citability`: citation-readiness review
- `crawlers`: robots and AI crawler access
- `llmstxt`: `llms.txt` generation and validation
- `brands`: brand and fact consistency review
- `platforms`: platform-specific AI optimization
- `schema`: structured data analysis
- `technical`: technical SEO floor
- `content`: content quality and freshness
- `report`: executive and client reporting
- `compare`: recurring checks and delta tracking

## CLI

```bash
python scripts/geo_command_surface.py catalog
python scripts/geo_command_surface.py audit --format json
```

## API

- `GET /api/v1/tools/command-catalog`
- `POST /api/v1/tools/command-router`

This is intentionally a routing layer, not a new hidden scoring engine.
