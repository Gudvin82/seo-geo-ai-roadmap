# Реальные Кейсы

Этот файл не заявляет private customer telemetry. Он моделирует, как
методология репозитория читает три публичных сайта по открытым сигналам и
честной ручной оценке. Числа ниже — это прозрачные snapshot scores, а не
завышенные claims об успехе.

Модель scoring в этом файле:

- Technical SEO и crawl readiness: `0-20`
- Factual consistency и truth-center discipline: `0-20`
- Entity clarity и trust proof: `0-20`
- AI readiness и answer extraction: `0-20`
- Reporting и operator packaging: `0-20`

## sitepravo.ru

Публично наблюдаемые сигналы:

- legal-service positioning выражено явно
- на сайте заявлены `570+` параметров и `15` направлений
- видны юридические документы, данные оператора и policy links
- уже присутствует cross-linking с sister entities

### Snapshot score SitePravo

- Technical SEO и crawl readiness: `16/20`
- Factual consistency и truth-center discipline: `15/20`
- Entity clarity и trust proof: `18/20`
- AI readiness и answer extraction: `16/20`
- Reporting и operator packaging: `17/20`
- Total public snapshot: `82/100`

### Ограниченная before/after модель SitePravo

- До первого v3-style pass: `82/100`
- После первой 30-day цели по truth-center и AI-surface sync: `88/100`
- Ожидаемая дельта: `+6`

Вероятные источники роста:

- свести повторяющиеся fact surfaces к одному canonical truth center
- жестче развести cross-entity boundaries с `anmalishev.ru` и sibling products
- синхронизировать numeric claims между главной, metadata, docs и AI-facing
  files

## auditguard.ru

Публично наблюдаемые сигналы:

- public-first framing технического аудита понятен сразу
- на homepage явно показаны `340+` параметров, `46+` tools и проверки за `2-5`
  минут
- сервис объясняет scope, legal basis и boundary "только публичный контур"
- trust и evidence framing сильные

### Snapshot score AuditGuard

- Technical SEO и crawl readiness: `17/20`
- Factual consistency и truth-center discipline: `14/20`
- Entity clarity и trust proof: `16/20`
- AI readiness и answer extraction: `15/20`
- Reporting и operator packaging: `18/20`
- Total public snapshot: `80/100`

### Ограниченная before/after модель AuditGuard

- До первого v3-style pass: `80/100`
- После первой 30-day цели по fact-sync и entity-governance: `86/100`
- Ожидаемая дельта: `+6`

Вероятные источники роста:

- более жесткая синхронизация между public copy, evidence pages и AI-facing
  files
- более четкое разделение AuditGuard и окружающей product ecosystem
- более сильная benchmark-reporting дисциплина внутри self-hosted app flow

## anmalishev.ru

Публично наблюдаемые сигналы:

- founder identity, legal details и location указаны явно
- RU и EN service surfaces уже видны
- сайт связывает consulting, products, case studies и methodology assets
- позиционирование "практический AI для бизнеса" звучит ясно и коммерчески
  предметно

### Snapshot score anmalishev.ru

- Technical SEO и crawl readiness: `15/20`
- Factual consistency и truth-center discipline: `14/20`
- Entity clarity и trust proof: `17/20`
- AI readiness и answer extraction: `17/20`
- Reporting и operator packaging: `15/20`
- Total public snapshot: `78/100`

### Ограниченная before/after модель anmalishev.ru

- До первого v3-style pass: `78/100`
- После первой 30-day цели по entity-hierarchy и bilingual fact-sync: `85/100`
- Ожидаемая дельта: `+7`

Вероятные источники роста:

- более явное разделение founder entity, offers, products и frameworks
- единый canonical fact layer для legal, service и product claims
- более явные AI-facing truth surfaces для multilingual routing

## Общие выводы

- factual consistency — это отдельная подсистема, а не примечание на полях
- public proof важнее там, где несколько связанных сущностей активно
  cross-link'аются
- двуязычная discoverability лучше работает, когда EN и RU ведутся как
  production layers
- AI visibility дает лучший результат, когда усиливает technical SEO, а не
  пытается ее заменить

См. также:

- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)
- [docs/ru/canonical-facts-and-entity-consistency.md](./docs/ru/canonical-facts-and-entity-consistency.md)
- [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
