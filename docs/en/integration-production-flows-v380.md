# Integration Production Flows v3.8.0

`v3.8.0` promotes integrations from starter references into production-guided
flows.

## Covered sources

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

Each contract now states:

- readiness tier
- sync or execution mode
- required env vars
- CI workflow path
- next step

## Production-grade rule

The repository still stays review-first. Production-grade here means:

- repeatable
- exportable
- CI-aware
- explicitly gated
- honest about human approval boundaries
