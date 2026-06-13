# Command Catalog v3.8.0

`v3.8.0` усиливает command surface от простого каталога до канонического
`/geo ...` operator interface.

## Канонический путь

- `/geo quick`
- `/geo audit`
- `/geo graph`
- `/geo report`
- `/geo compare`

## Поддерживающие команды

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

## Почему это важно

Репозиторий становится проще и для человека, и для IDE-агента, когда intent,
aliases, outputs и use cases описаны явно.
