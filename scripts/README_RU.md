# Справочник По Скриптам

## Обзор

| Скрипт | Назначение | Пример |
|---|---|---|
| `generate_llms_txt.py` | Генерирует `llms.txt` из sitemap | `python scripts/generate_llms_txt.py --sitemap-url https://example.com/sitemap.xml` |
| `check-llms-txt.py` | Проверяет структуру `llms.txt` по файлу или URL | `python scripts/check-llms-txt.py --file examples/sample-llms.txt` |
| `check-robots-ai-bots.py` | Проверяет доступ AI/search-ботов в `robots.txt` | `python scripts/check-robots-ai-bots.py --url https://example.com` |
| `check-ai-txt.py` | Проверяет `ai.txt` и ищет противоречия с `robots.txt` / `llms.txt` | `python scripts/check-ai-txt.py --url https://example.com` |
| `sitemap-checker.py` | Загружает sitemap и считает URL | `python scripts/sitemap-checker.py --url https://example.com/sitemap.xml` |
| `schema-validator.py` | Проверяет JSON schema-файлы | `python scripts/schema-validator.py --file templates/schema/service-schema.json` |
| `schema-coverage-checker.py` | Аудирует покрытие JSON-LD schema на реальной странице | `python scripts/schema-coverage-checker.py --url https://example.com --site-type service` |
| `faq-detector.py` | Ищет FAQ и answer-ready patterns в HTML страницы | `python scripts/faq-detector.py --url https://example.com` |
| `open-graph-checker.py` | Проверяет полноту Open Graph и Twitter Card | `python scripts/open-graph-checker.py --url https://example.com` |
| `ai_readability_audit.py` | Аудирует AI readability layers: видимую структуру, schema, FAQ и guidance files | `python scripts/ai_readability_audit.py --url https://example.com` |
| `citability_score.py` | Считает heuristic citation-readiness score и quick wins | `python scripts/citability_score.py --url https://example.com --site-type service` |
| `check_cdn_blocking.py` | Проверяет, не блокирует ли edge-слой major AI bots | `python scripts/check_cdn_blocking.py --url https://example.com` |
| `rag_chunk_audit.py` | Проверяет, насколько контент готов к RAG chunking | `python scripts/rag_chunk_audit.py --url https://example.com/article` |
| `crux_field_data.py` | Загружает или валидирует CrUX field-data payload | `python scripts/crux_field_data.py --url https://example.com` |
| `integration_verification_matrix.py` | Строит integration и CMS verification matrix | `python scripts/integration_verification_matrix.py --json` |
| `robots-sitemap-link-checker.py` | Проверяет связку robots.txt и sitemap вместе | `python scripts/robots-sitemap-link-checker.py --url https://example.com` |
| `ai-share-of-voice-tracker.py` | Создает заготовки для учета AI Share of Voice | `python scripts/ai-share-of-voice-tracker.py "Example AI Agency" --queries "best GEO agency,ai visibility audit"` |
| `serp-intent-cluster-helper.py` | Группирует ключевые фразы по rough intent | `python scripts/serp-intent-cluster-helper.py "best ai agency" "what is geo"` |
| `content-inventory-helper.py` | Создает markdown-таблицу инвентаризации контента по URL | `python scripts/content-inventory-helper.py https://example.com/ https://example.com/faq` |
| `roi_calculator.py` | Считает ROI / ROMI для SEO и AI-трафика | `python scripts/roi_calculator.py --traffic 5000 --conversion-rate 0.03 --lead-to-sale-rate 0.2 --average-check 1200 --margin-rate 0.45 --seo-cost 1500` |
| `content_freshness_checker.py` | Классифицирует URL из sitemap как fresh, stale или unknown | `python scripts/content_freshness_checker.py --sitemap-url https://example.com/sitemap.xml --days-stale 180 --output-file freshness.md` |
| `check_hallucinations.py` | Создает стартовый отчет для проверки AI-галлюцинаций | `python scripts/check_hallucinations.py --brand-facts-file examples/brand-facts-example.md --questions-file examples/hallucination-questions-example.md --output-file hallucination-report.md` |
| `gsc_data_stub.py` | Выдает starter-payload в форме Google Search Console | `python scripts/gsc_data_stub.py` |
| `yandex_data_stub.py` | Выдает starter-payload в форме Яндекс-данных | `python scripts/yandex_data_stub.py` |
| `provider_benchmark_stub.py` | Печатает scaffold для benchmark-оценки провайдеров | `python scripts/provider_benchmark_stub.py` |
| `fact_drift_checker.py` | Сравнивает brand facts между поверхностями и ищет drift-паттерны | `python scripts/fact_drift_checker.py --surface website=./website.md --surface schema=./schema.md` |
| `scheduled_check_runner.py` | Печатает execution plan для регулярной проверки | `python scripts/scheduled_check_runner.py --project-id 1 --check-type llms --frequency weekly --schedule-mode github_actions` |
| `geo_command_surface.py` | Маршрутизирует GEO/SEO/AI-задачи к нужным scripts, docs и API routes | `python scripts/geo_command_surface.py audit --format json` |
| `bootstrap_self_hosted.py` | Печатает bootstrap-план для demo или production-like self-hosted установки | `python scripts/bootstrap_self_hosted.py --mode demo --format markdown` |

## `generate_llms_txt.py`

- Назначение: собрать черновик `llms.txt` из sitemap по URL или локальному файлу.
- Параметры:
  - `--sitemap-url`
  - `--sitemap-file`
  - `--output-file`
- Пример запуска:

```bash
python scripts/generate_llms_txt.py \
  --sitemap-url https://example.com/sitemap.xml \
  --output-file ./llms.txt
```

- Ожидаемый вывод:
  - источник sitemap
  - число обработанных / включенных / пропущенных URL
  - путь к выходному файлу
  - warnings по URL с общими описаниями
- Частые ошибки:
  - не передан ни `--sitemap-url`, ни `--sitemap-file`
  - локальный файл недоступен
  - сеть не дает скачать sitemap
  - XML битый
  - из sitemap не извлеклось ни одного URL
- Ограничения:
  - описания выводятся по эвристикам и требуют ревью
  - `/tag/` и `/author/` пропускаются по умолчанию

## `check-llms-txt.py`

- Назначение: быстро проверить, есть ли в `llms.txt` базовые ожидаемые секции.
- Параметры:
  - `--url`
  - `--file`
- Пример запуска:

```bash
python scripts/check-llms-txt.py --file examples/sample-llms.txt
```

- Ожидаемый вывод:
  - число непустых строк
  - `PASS` или `FAIL`
  - список отсутствующих секций при ошибке
- Частые ошибки:
  - файл не найден
  - URL недоступен
  - нет упоминаний `faq` или `about`
- Ограничения:
  - это легкая структурная проверка, а не полный аудит содержания

## `check-robots-ai-bots.py`

- Назначение: посмотреть, открыт ли `robots.txt` для ключевых AI/search-ботов.
- Параметры:
  - `--url`
- Пример запуска:

```bash
python scripts/check-robots-ai-bots.py --url https://example.com
```

- Ожидаемый вывод:
  - какой `robots.txt` был использован
  - markdown-таблица по ботам, статусам и рекомендациям
- Частые ошибки:
  - `robots.txt` недоступен
  - правила частичные или неоднозначные
- Ограничения:
  - сложные path-based rules все равно нужно читать вручную

## `sitemap-checker.py`

- Назначение: скачать sitemap и посчитать количество URL в XML.
- Параметры:
  - `--url`
- Пример запуска:

```bash
python scripts/sitemap-checker.py --url https://example.com/sitemap.xml
```

- Ожидаемый вывод:
  - общее число URL
- Частые ошибки:
  - сеть
  - битый XML
- Ограничения:
  - проверяет доступность и count, но не качество sitemap

## `schema-validator.py`

- Назначение: проверить, парсится ли JSON schema-файл.
- Параметры:
  - `--file`
- Пример запуска:

```bash
python scripts/schema-validator.py --file templates/schema/service-schema.json
```

- Ожидаемый вывод:
  - `Valid JSON`
- Частые ошибки:
  - файл отсутствует
  - синтаксическая ошибка в JSON
- Ограничения:
  - проверяется JSON, а не внешняя семантическая валидность schema.org

## `ai-share-of-voice-tracker.py`

- Назначение: подготовить markdown или CSV-заготовку для AI Share of Voice.
- Параметры:
  - позиционный `brand`
  - `--queries`
  - `--format`
  - `--output`
- Пример запуска:

```bash
python scripts/ai-share-of-voice-tracker.py \
  "Example AI Agency" \
  --queries "best GEO agency,ai visibility audit" \
  --format markdown
```

- Ожидаемый вывод:
  - таблица markdown или CSV-строки для повторяемого мониторинга
- Частые ошибки:
  - пустой список запросов
  - не передан `--output` для CSV
- Ограничения:
  - инструмент рассчитан на ручной или полуавтоматический сбор

## `serp-intent-cluster-helper.py`

- Назначение: грубо разложить ключевые фразы по intent-кластерам.
- Параметры:
  - позиционные keyword-фразы
- Пример запуска:

```bash
python scripts/serp-intent-cluster-helper.py \
  "best ai agency" \
  "what is geo" \
  "ai visibility price"
```

- Ожидаемый вывод:
  - markdown-таблица с группировкой по intent
- Частые ошибки:
  - не переданы ключевые фразы
- Ограничения:
  - это эвристика, а не замена полноценного SERP-анализа

## `content-inventory-helper.py`

- Назначение: быстро собрать markdown-таблицу инвентаризации контента по URL.
- Параметры:
  - позиционные URL
- Пример запуска:

```bash
python scripts/content-inventory-helper.py \
  https://example.com/ \
  https://example.com/faq \
  https://example.com/services/ai-visibility
```

- Ожидаемый вывод:
  - пустая структура таблицы для content inventory
- Частые ошибки:
  - URL не переданы
- Ограничения:
  - intent, funnel и ownership нужно размечать вручную

## `roi_calculator.py`

- Назначение: оценить visits, leads, sales, revenue, gross margin и ROI / ROMI.
- Параметры:
  - `--traffic`
  - `--conversion-rate`
  - `--lead-to-sale-rate`
  - `--average-check`
  - `--margin-rate`
  - `--seo-cost`
  - `--ai-referred-share`
  - `--period`
- Пример запуска:

```bash
python scripts/roi_calculator.py \
  --traffic 5000 \
  --conversion-rate 0.03 \
  --lead-to-sale-rate 0.2 \
  --average-check 1200 \
  --margin-rate 0.45 \
  --seo-cost 1500 \
  --ai-referred-share 0.1 \
  --period monthly
```

- Ожидаемый вывод:
  - visits
  - AI-referred visits
  - leads
  - sales
  - revenue
  - gross margin
  - cost
  - estimated ROI / ROMI
- Частые ошибки:
  - пропущены обязательные numeric inputs
  - пользователь подает нереалистичные rate values
- Ограничения:
  - это инструмент для планирования, а не полная модель атрибуции
  - удобно использовать вместе с [templates/roi-model-template-ru.md](../templates/roi-model-template-ru.md)

## `content_freshness_checker.py`

- Назначение: классифицировать URL из sitemap как fresh, stale или unknown freshness.
- Параметры:
  - `--sitemap-url`
  - `--sitemap-file`
  - `--days-stale`
  - `--output-file`
  - `--format markdown|csv|json`
- Пример запуска:

```bash
python scripts/content_freshness_checker.py \
  --sitemap-url https://example.com/sitemap.xml \
  --days-stale 180 \
  --output-file ./freshness-report.md \
  --format markdown
```

- Ожидаемый вывод:
  - URL
  - detected `lastmod`
  - status
  - recommendation
- Частые ошибки:
  - sitemap недоступен
  - XML битый
  - не извлеклось ни одного URL
  - для CSV не передан `--output-file`
- Ограничения:
  - качество зависит от корректности `lastmod` в sitemap
  - см. [examples/content-freshness-report-example.md](../examples/content-freshness-report-example.md)

## `check_hallucinations.py`

- Назначение: собрать starter-отчет по проверке AI-галлюцинаций на базе
  canonical brand facts и набора вопросов.
- Параметры:
  - `--brand-facts-file`
  - `--questions-file`
  - `--output-file`
  - `--format markdown|csv|json`
  - optional `--provider`
  - optional `--model`
- Пример запуска:

```bash
python scripts/check_hallucinations.py \
  --brand-facts-file examples/brand-facts-example.md \
  --questions-file examples/hallucination-questions-example.md \
  --output-file ./hallucination-report.md \
  --format markdown
```

- Ожидаемый вывод:
  - question
  - expected facts
  - answer placeholder
  - discrepancy status
  - next action
- Частые ошибки:
  - отсутствуют входные файлы
  - не распарсились вопросы
  - нечитабельный JSON или markdown
- Ограничения:
  - provider integration остается optional и intentionally lightweight
  - особенно полезен вместе с [templates/brand-facts-template-ru.md](../templates/brand-facts-template-ru.md)
