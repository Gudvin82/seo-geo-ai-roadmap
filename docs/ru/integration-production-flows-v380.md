# Integration Production Flows v3.8.0

`v3.8.0` переводит integrations из starter-референсов в production-guided
flows.

## Какие источники покрыты

- Google Search Console
- GA4
- Yandex Webmaster
- Yandex Metrica
- WordPress
- Webflow
- Bitrix
- Tilda

## Machine-readable contracts

- `GET /api/v1/integrations/contracts`
- `GET /api/v1/cms/contracts`
- `GET /api/v1/tools/command-contract`

Теперь каждый контракт явно содержит:

- readiness tier
- sync или execution mode
- required env vars
- путь до CI workflow
- следующий шаг

## Что здесь значит production-grade

Репозиторий все еще остается review-first. Production-grade здесь значит:

- повторяемость
- экспортируемость
- CI-aware контур
- явные gating rules
- честная граница human approval
