# Technical SEO Deep Playbook

Этот playbook нужен, чтобы “проверить canonical и sitemap” превратилось в
реальный operator workflow.

## Когда использовать

- сайт новый, восстанавливается или перестраивается
- страницы плохо индексируются или просели
- сайт сильно зависит от JS
- AI visibility выглядит слабой из-за неясного технического слоя

## Что проверять в первую очередь

1. response codes приоритетных страниц
2. согласованность canonical
3. robots rules
4. чистоту sitemap
5. internal linking в money pages
6. rendering и наличие server HTML
7. Core Web Vitals и вес ассетов
8. redirect chains и duplicate URL surfaces

## Как выглядит “хорошо”

- все важные страницы отдают `200`
- canonical указывает на реально нужную индексируемую страницу
- robots rules закрывают только непубличные или низкоценные поверхности
- sitemap содержит canonical, indexable и актуальные URL
- server HTML несет критический business meaning страницы
- money pages получают ссылки из релевантных hub pages
- CWV не ломают high-intent experience

## Типовые сбои

### Конфликт canonical

Симптомы:

- canonical ведет на другую страницу
- пагинация или фильтры схлопываются не туда
- локализованные страницы canonical-ятся на default language

Что делать:

- описать canonical-правило для каждого page type
- явно зафиксировать исключения: filters, tags, language variants
- проверять итоговый HTML, а не только CMS-настройку

### Загрязненный sitemap

Симптомы:

- старые URL еще лежат в sitemap
- redirected URLs до сих пор перечислены
- есть thin utility pages
- присутствуют duplicate language или parameter URLs

Что делать:

- выгрузить текущий sitemap
- разбить URL по типам страниц
- удалить redirected, blocked, duplicate и non-canonical entries
- оставить чистый canonical sitemap

### JavaScript SEO gap

Симптомы:

- raw HTML тонкий
- контент появляется только после hydration
- structured data вставляется поздно или нестабильно
- AI или crawler heuristics видят меньше, чем пользователь

Что делать:

- сначала смотреть raw HTML
- выносить title, headings, critical copy, facts и schema на server side
- не опираться на client-side rendering для business meaning страницы

### Слабый internal linking

Симптомы:

- важные коммерческие страницы почти не получают контекстных ссылок
- блог и support контент не передают релевантность на service pages
- hubs есть визуально, но не семантически

Что делать:

- построить карту hub → service → proof → conversion
- следить за понятным anchor language
- в первую очередь усиливать ссылки на revenue-critical и entity-critical pages

## Приоритет исправлений

Сначала чинить:

1. indexing и crawl blockers
2. неправильный canonical
3. rendering gaps на money pages
4. загрязнение sitemap
5. internal-linking gaps
6. CWV и redirect optimization

## Proof и QA

Для каждого изменения сохраняйте:

- before state
- after state
- затронутую страницу или template
- validation method
- ожидаемый business или discoverability effect

Technical SEO нельзя считать готовым без proof.

## С чем сочетать

- [../05-technical-seo.md](./05-technical-seo.md)
- [../../checklists/ru/technical-seo-checklist.md](../../checklists/ru/technical-seo-checklist.md)
- [./scoring-model-v340.md](./scoring-model-v340.md)
