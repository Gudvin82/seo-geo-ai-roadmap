# Command Catalog

`v3.4.0` добавляет command surface, чтобы и человек, и AI agent могли быстро
сопоставить широкую GEO-задачу с нужными scripts, docs и API routes.

## Базовые команды

- `audit`: полный GEO и SEO audit flow
- `quick`: быстрый starter snapshot
- `citability`: review citation-readiness
- `crawlers`: robots и AI crawler access
- `llmstxt`: генерация и валидация `llms.txt`
- `brands`: review brand и fact consistency
- `platforms`: platform-specific AI optimization
- `schema`: анализ structured data
- `technical`: technical SEO floor
- `content`: content quality и freshness
- `report`: executive и client reporting
- `compare`: регулярные проверки и delta tracking

## CLI

```bash
python scripts/geo_command_surface.py catalog
python scripts/geo_command_surface.py audit --format json
```

## API

- `GET /api/v1/tools/command-catalog`
- `POST /api/v1/tools/command-router`

Это routing layer, а не новый скрытый scoring engine.
