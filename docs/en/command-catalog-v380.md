# Command Catalog v3.8.0

`v3.8.0` upgrades the command surface from a simple catalog into a canonical
`/geo ...` operator interface.

## Canonical path

- `/geo quick`
- `/geo audit`
- `/geo graph`
- `/geo report`
- `/geo compare`

## Supporting commands

- `/geo deploy`
- `/geo scanner`
- `/geo crawlers`
- `/geo llmstxt`
- `/geo brands`
- `/geo platforms`
- `/geo schema`
- `/geo technical`
- `/geo content`
- `/geo citability`

## CLI

```bash
python scripts/geo_command_surface.py catalog --format markdown
python scripts/geo_command_surface.py "/geo audit" --format json
python scripts/geo_command_surface.py graph --format markdown
```

## Why this matters

The repository becomes easier for humans and IDE agents when intent, aliases,
outputs, and use cases are explicit.
