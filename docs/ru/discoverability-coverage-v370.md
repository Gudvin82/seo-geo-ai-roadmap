# Discoverability Coverage в v3.7.0

`v3.7.0` расширяет practical discoverability coverage layer поверх scanner
foundation.

## Что теперь проверяется

- RU и AI bot policy, включая `YandexAdditional`
- структура и consistency hints для `ai.txt`
- покрытие JSON-LD schema, включая `WebSite`
- FAQ и answer-ready patterns
- полнота Open Graph и Twitter Card
- связка `robots.txt` ↔ sitemap

## Почему это важно

Это общий hygiene-слой для SEO, GEO, RU-search и AI discoverability. Эти
проверки не гарантируют rankings или citations, но уменьшают двусмысленность и
дают оператору более конкретную поверхность для review.

## Доступные скрипты

```bash
python scripts/check-robots-ai-bots.py --url https://example.com
python scripts/check-ai-txt.py --url https://example.com
python scripts/schema-coverage-checker.py --url https://example.com --site-type service
python scripts/faq-detector.py --url https://example.com
python scripts/open-graph-checker.py --url https://example.com
python scripts/robots-sitemap-link-checker.py --url https://example.com
```

## Reporting model

Каждый модуль должен давать:

- observed fact
- inferred issue
- recommendation
- limitation или uncertainty

Уровни severity:

- `pass`
- `info`
- `warn`
- `fail`
- `needs-review`

## Текущие ограничения

- FAQ detector эвристический
- Open Graph checks не доказывают реальный social rendering
- schema coverage фокусируется на JSON-LD, а не на полном microdata parsing
- `ai.txt` остается emergent pattern, а не гарантированным стандартом
- проверка `YandexAdditional` читает `robots.txt`, но не доказывает inclusion в Яндекс.Нейро
