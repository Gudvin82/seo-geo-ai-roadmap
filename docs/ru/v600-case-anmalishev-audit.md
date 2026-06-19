# Кейс: публичный аудит anmalishev.ru в v6

Этот кейс следует той же evidence-политике, что и остальной репозиторий:

- только public observations
- только bounded script outputs
- без private analytics claims
- с явным разделением между реальной силой сайта и ограничениями детектора

## Сайт

- URL: <https://anmalishev.ru/>
- Рынок: RU-first с EN surfaces
- Тип: personal brand + AI services + product surfaces

## Что проверялось

- raw HTML homepage
- `robots.txt`
- `sitemap.xml`
- `llms.txt`
- `ai.txt`
- Open Graph и Twitter metadata
- schema coverage
- FAQ detectability
- AI readability
- citability heuristic
- RAG chunk readiness heuristic

## Сильные сигналы

- canonical присутствует
- hreflang присутствует
- Open Graph и Twitter поля заполнены
- присутствуют Person, LocalBusiness, Service, WebSite и FAQ schema
- `llms.txt` публичный и валидный
- `ai.txt` публичный и согласованный
- `robots.txt` публичный, явный и AI-aware
- local и RU trust signals сильные

## Результаты scripts

- `check-llms-txt.py`: `PASS`
- `check-ai-txt.py`: `PASS`
- `open-graph-checker.py`: `PASS`
- `faq-detector.py`: `WARN`
- `schema-coverage-checker.py`: `WARN`
- `ai_readability_audit.py`: `WARN`, `50/100`
- `citability_score.py`: `WARN`, `55/100`
- `rag_chunk_audit.py`: `FAIL`

## Почему слабые heuristic scores не описывают всю картину

Сайт сильнее, чем показывают raw heuristic scores.

Главная причина:

- значимая часть контента частично завязана на client-rendered product layer
- bounded HTML detectors видят меньше структуры, чем реальный пользователь
- FAQ schema есть, но visible answer-ready layout недостаточно явно читается детектором

Это реальный operating lesson:

- GEO и AI heuristics нельзя путать с полной реальностью
- но они все равно дают полезный improvement path

## Ограниченная интерпретация

### SEO foundation

Сильная.

Технический baseline у сайта уже выше среднего для founder-led surface:

- canonical
- hreflang
- raw metadata
- public sitemap
- AI-facing files
- trust и legal structure

### GEO и AI readability

Смешанная.

Facts и machine-readable assets хорошие, но answer-ready structure и
server-visible chunking еще можно усиливать.

### Local и RU readiness

Сильная.

Сайт ясно передает geography, entity identity, legal trust и Yandex-relevant
market framing.

## Приоритетные улучшения

1. вынести больше visible FAQ и answer-ready HTML в server response
2. добавить `Organization` schema рядом с текущими сущностями там, где это усиливает интерпретацию
3. добавить `BreadcrumbList` там, где важна навигационная иерархия
4. усилить heading-led chunk structure на ключевых коммерческих страницах
5. держать AI-facing files синхронизированными с truth center сайта

## Почему этот кейс важен

Он показывает, что репозиторий ведет себя честно:

- public facts уже могут давать сильный результат
- heuristics могут недочитывать JS-heavy page
- bounded scripts полезны, но operator interpretation все еще необходима
