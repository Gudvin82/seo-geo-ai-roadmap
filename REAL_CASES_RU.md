# Реальные Кейсы

Этот файл не заявляет private customer telemetry. Он объединяет:

- текущие public signals, которые можно проверить сейчас
- bounded implementation records из процесса внедрения
- прозрачную оценку по методологии вместо завышенных success claims

Модель scoring в этом файле:

- Technical SEO и crawl readiness: `0-20`
- Factual consistency и truth-center discipline: `0-20`
- Entity clarity и trust proof: `0-20`
- AI readiness и answer extraction: `0-20`
- Reporting и operator packaging: `0-20`

Подробные кейсы:

- [anmalishev.ru — public before / after case](./docs/ru/v430-case-anmalishev.md)
- [auditguard.ru + sitepravo.ru — AI crawler access и public before / after case](./docs/ru/v430-case-auditguard-sitepravo.md)

## sitepravo.ru

Текущие публично наблюдаемые сигналы:

- legal-service positioning выражено явно
- на сайте заявлены `570+` параметров и `15` направлений
- видны юридические документы, данные оператора и policy links
- `robots.txt` теперь явно разрешает целевой AI crawler set, включая `ClaudeBot` и `YandexAdditional`

### Текущий snapshot

- Current public snapshot: `88/100`
- Current findings count в bounded rollout model: `14`
- Current explicit AI-bot allow coverage в rollout records: `14/14`

### Ограниченный before / after implementation record

- До GEO AI crawler hardening: `88/100`
- После GEO AI crawler hardening: `88/100`
- Findings delta в rollout record: `15 -> 14`
- Explicit AI-bot allow coverage в rollout record: `6/14 -> 14/14`

Интерпретация:

- score не вырос, потому что public product report для этой поверхности GEO-слой почти не взвешивает
- при этом AI crawler access реально улучшился
- это хороший пример “реального discoverability-улучшения без vanity-metric inflation”

## auditguard.ru

Текущие публично наблюдаемые сигналы:

- public-first framing технического аудита понятен сразу
- на homepage явно показаны `340+` параметров, `46+` tools и проверки за `2-5` минут
- сервис объясняет scope, legal basis и boundary "только публичный контур"
- `llms.txt` подробный и публичный
- `robots.txt` теперь явно разрешает целевой AI crawler set, включая `ClaudeBot` и `YandexAdditional`

### Текущий snapshot

- Current public snapshot: `94/100`
- Current findings count в bounded rollout model: `11`
- Current explicit AI-bot allow coverage в rollout records: `14/14`

### Ограниченный before / after implementation record

- До AI crawler hardening и false-positive cleanup: `92/100`
- После AI crawler hardening и false-positive cleanup: `94/100`
- Findings delta в rollout record: `13 -> 11`
- Explicit AI-bot allow coverage в rollout record: `6/14 -> 14/14`

Интерпретация:

- intent для AI crawlers стал заметно яснее
- false-positive leak findings вокруг `llms.txt` и `ai.txt` убраны
- рост подтверждается и bounded score, и текущим public `robots.txt`

## anmalishev.ru

Текущие публично наблюдаемые сигналы:

- founder identity, legal details и location указаны явно
- RU и EN service surfaces уже видны
- сайт связывает consulting, products, case studies и methodology assets
- текущий `sitemap.xml` включает усиленные canonical surfaces: `/contacts`, `/projects/seo-geo-ai-roadmap.html`, `/expert/yandex-neuro-ai-visibility.html` и `/expert/ai-site-audit.html`
- текущие `llms.txt` и `ai.txt` согласованы и публичны
- текущий `robots.txt` сохраняет public AI и search surfaces открытыми, при этом закрывает admin и raw-template paths

### Текущий snapshot

- Current public snapshot: `88/100`

### Ограниченный before / after implementation record

- До June public-surface expansion: `79/100`
- После June public-surface expansion: `88/100`
- Methodology delta: `+9`

Публично видимые источники роста:

- более сильный homepage entity и trust graph
- выделенная canonical contacts surface
- выделенная Yandex AI / Neuro page
- выделенная AI site audit page
- выделенная repository-overview page
- более плотная согласованность между `llms.txt`, `ai.txt`, `robots.txt` и `sitemap.xml`

## Общие выводы

- factual consistency — это отдельная подсистема, а не примечание на полях
- public proof важнее там, где несколько связанных сущностей активно cross-link'аются
- двуязычная discoverability лучше работает, когда EN и RU ведутся как production layers
- AI visibility дает лучший результат, когда усиливает technical SEO, а не пытается ее заменить
- явная AI crawler policy может давать реальный public delta, даже если продуктовый score это пока отражает слабо
- сильный кейс должен отделять current public facts от bounded rollout records и от непроверенных private outcomes

См. также:

- [docs/en/ai-citation-score.md](./docs/en/ai-citation-score.md)
- [docs/ru/canonical-facts-and-entity-consistency.md](./docs/ru/canonical-facts-and-entity-consistency.md)
- [docs/ru/v430-review-response-and-upgrade-path.md](./docs/ru/v430-review-response-and-upgrade-path.md)
- [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)
