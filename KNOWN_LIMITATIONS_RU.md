# Known Limitations

## Что уже production-ready

- self-hosted FastAPI-приложение с demo seed и migrations
- прозрачная генерация reports и artifacts
- EN/RU документация и operator-guidance
- модель конфигурации cloud и local AI providers

## Что уже usable, но еще MVP

- workspace roles и invite flow
- canonical audit execution endpoint
- audit log и расширенные metrics
- статический frontend operator console

## Что пока experimental

- local LLM adapters (`ollama`, `localai`, `vllm`) зависят от внешнего runtime
- patch-mode пока artifact-first, а не прямой CMS writeback
- cloud manifests пока starter-уровня, а не hosted support contract

## Что в roadmap

- более явная queue/retry-модель
- более глубокая CMS write-поддержка
- более сильный export/import слой
- более детальная project-level permission model
