# Кейс: auditguard.ru и sitepravo.ru — AI crawler access, public before / after и bounded score interpretation

Date: 2026-06-14
Methodology source: <https://github.com/Gudvin82/seo-geo-ai-roadmap>

## Почему эти два сайта важны

Эти два сайта показывают полезный паттерн:

- `auditguard.ru` показывает измеримый рост score и снижение findings
- `sitepravo.ru` показывает реальное улучшение AI discoverability даже там, где product score почти не двигается

Это важно. Не каждое реальное discoverability-улучшение нужно насильно
запихивать в vanity metric.

## Current public verification

Публично в текущий момент проверяется:

- оба сайта отдают public `robots.txt`
- оба сайта явно разрешают целевой AI crawler set, включая:
  - `GPTBot`
  - `ChatGPT-User`
  - `PerplexityBot`
  - `ClaudeBot`
  - `Google-Extended`
  - `Applebot-Extended`
  - `YandexAdditional`
  - а также дополнительные commercial или research crawlers, например `Amazonbot`, `Diffbot` и `cohere-ai`
- `auditguard.ru` также отдает подробный public `llms.txt`
- `sitepravo.ru` также отдает подробный public `llms.txt`

Важная оговорка:

- current public files доказывают after-state
- before-state — это implementation record из процесса внедрения

## auditguard.ru

### auditguard.ru до

- качественные `llms.txt` и `ai.txt` уже существовали
- только `6/14` ключевых AI bots имели explicit allow rules в rollout records
- несколько значимых bots все еще были `unspecified`
- detector также давал false-positive “leak” findings вокруг публичных AI-facing files

### auditguard.ru после

- все `14/14` target AI bots стали explicitly allowed в rollout records
- false-positive leak interpretation была убрана
- текущий public `robots.txt` отражает более сильную AI crawler policy

### auditguard.ru bounded before / after

| Метрика | До | После | Delta |
|---|---:|---:|---:|
| Overall score | 92 | 94 | +2 |
| Total findings | 13 | 11 | -2 |
| `robots.txt`: explicit AI-bot allow coverage | 6/14 | 14/14 | +8 bots |

### Интерпретация auditguard.ru

Это хороший пример реального GEO-layer improvement, который не сводится только
к content changes:

- у сайта уже были сильные trust и public-product framing
- delta пришла из более ясной crawler policy и более чистой интерпретации
- public AI discoverability стала более явной и менее двусмысленной

## sitepravo.ru

### sitepravo.ru до

- для этой legal-first поверхности GEO block слабо отражался в product score
- rollout records все еще показывали только `6/14` key AI bots как explicitly allowed

### sitepravo.ru после

- explicit AI crawler coverage дошла до `14/14` в rollout records
- текущий public `robots.txt` подтверждает clear allows для target AI set
- total findings снизились на один в bounded rollout record

### sitepravo.ru bounded before / after

| Метрика | До | После | Delta |
|---|---:|---:|---:|
| Overall score | 88 | 88 | 0 |
| Total findings | 15 | 14 | -1 |
| `robots.txt`: explicit AI-bot allow coverage | 6/14 | 14/14 | +8 bots |

### Интерпретация sitepravo.ru

Это более тонкий кейс:

- реальный AI discoverability layer улучшился
- visible top-line score не изменился
- это не failure, а пример того, что scoring model нельзя путать со всей системой реальности

## Общий вывод по двум кейсам

Вместе эти два сайта показывают один практический урок:

- explicit AI crawler policy важна
- двусмысленность в `robots.txt` может быть реальным operational gap
- public AI-facing files нельзя автоматически маркировать как leaks
- часть улучшений напрямую поднимает product score
- часть улучшений усиливает реальную discoverability раньше, чем score успевает это отразить

## Public URLs из кейса

- <https://auditguard.ru/robots.txt>
- <https://auditguard.ru/llms.txt>
- <https://sitepravo.ru/robots.txt>
- <https://sitepravo.ru/llms.txt>
