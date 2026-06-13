# Commands

`v3.4.0` introduced the command surface, and `v3.5.0` extends it with
deployment and scanner-oriented handoff flows.

Core routes:

- `audit`
- `quick`
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
python scripts/geo_command_surface.py audit --format json
python scripts/agent_handoff_pack.py --task audit-site --language en --target-url https://example.com
python scripts/bootstrap_self_hosted.py --mode demo --format markdown
python scripts/bootstrap_self_hosted.py --mode scanner --format markdown
```
