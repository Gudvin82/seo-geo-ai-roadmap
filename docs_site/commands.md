# Commands

`v3.8.0` turns the command surface into a canonical `/geo ...` operating layer.

Core path:

- `/geo quick`
- `audit`
- `/geo graph`
- `/geo report`
- `/geo compare`

Supporting routes:

- `citability`
- `crawlers`
- `deploy`
- `llmstxt`
- `brands`
- `platforms`
- `scanner`
- `schema`
- `technical`
- `content`
- `report`
- `compare`

Use the repository CLI:

```bash
python scripts/geo_command_surface.py catalog
python scripts/geo_command_surface.py "/geo audit" --format json
python scripts/geo_command_surface.py graph --format markdown
python scripts/agent_handoff_pack.py --task audit-site --language en --target-url https://example.com
python scripts/bootstrap_self_hosted.py --mode demo --format markdown
python scripts/bootstrap_self_hosted.py --mode scanner --format markdown
```

Machine-readable contracts:

- `GET /api/v1/tools/command-contract`
- `GET /api/v1/integrations/contracts`
- `GET /api/v1/cms/contracts`
