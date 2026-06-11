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
- prompt library UI, project export package и история AI SoV уже полезны, но пока легковесны
- webhook notifications пока starter-уровня и предполагают ваши собственные endpoints

## Что пока experimental

- local LLM adapters (`ollama`, `localai`, `vllm`) зависят от внешнего runtime
- patch-mode пока artifact-first, а не прямой CMS writeback
- cloud manifests пока starter-уровня, а не hosted support contract
- heuristic benchmark scoring пока starter-интерпретация, а не полноценная industry benchmark база
- интеграции с Google Search Console и Яндексом пока bootstrap-stubs, а не полный OAuth automation
- доставка уведомлений пока без durable retry queues и без гарантированной последовательности

## Что в roadmap

- более явная queue/retry-модель
- более глубокая CMS write-поддержка
- более сильный export/import слой
- более детальная project-level permission model
- production-grade webhook retry, scheduling и operator alerting
- более сильные benchmark-baselines по нишам, регионам и device mix
- более глубокий WordPress/CMS writeback с безопасными review gates
