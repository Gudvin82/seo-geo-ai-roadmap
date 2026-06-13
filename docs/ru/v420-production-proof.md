# v4.2.0 Production Proof и усиление платформы

`v4.2.0` усиливает ровно те зоны, которые раньше были средними, частичными или
отсутствовали:

- аудит AI readability
- scoring вероятности цитирования
- проверка CDN или edge-блокировок для AI-ботов
- проверка RAG chunk readiness
- путь для CrUX field data
- integration verification matrix
- расширенное покрытие провайдеров
- stack packs для WordPress, React и Angular

## Новые scanner-модули

- `ai_readability`
- `citability_score`
- `cdn_ai_bot_blocking`
- `rag_chunk_readiness`

Они доступны и через scanner в приложении, и через отдельные скрипты.

## Новые скрипты

- `python scripts/ai_readability_audit.py --url https://example.com`
- `python scripts/citability_score.py --url https://example.com`
- `python scripts/check_cdn_blocking.py --url https://example.com`
- `python scripts/rag_chunk_audit.py --url https://example.com/page`
- `python scripts/crux_field_data.py --url https://example.com`
- `python scripts/integration_verification_matrix.py --json`

## Слой integration proof

Теперь репозиторий отдает machine-readable verification matrix через:

- `GET /api/v1/integrations/verification-matrix?project_id={project_id}`

Каждая строка явно показывает текущее состояние:

- `contract_only`
- `starter_or_stub`
- `live_api_or_runtime`
- `live_inventory_or_reviewed_flow`

Это убирает расплывчатые обещания про “production-ready integrations”.

## Расширенные провайдеры

Cloud:

- OpenAI
- Anthropic
- Gemini
- Perplexity
- Mistral
- Cohere
- DeepSeek
- xAI / Grok

Local или self-hosted:

- Ollama
- LocalAI
- vLLM

## Stack packs

Новая папка `stack-packs/` дает AI-агентам и операторам более узкий,
CMS-aware стартовый слой:

- `stack-packs/wordpress.yaml`
- `stack-packs/react.yaml`
- `stack-packs/angular.yaml`

## Ограничения, которые остаются честными

- live GSC / GA4 / Yandex proof все еще зависит от реальных credentials и настройки оператора
- live CrUX режим зависит от `CRUX_API_KEY`
- citation score остается proxy-метрикой, а не обещанием упоминаний
- CDN bot checks это edge-probes, а не гарантия поведения краулеров во времени
