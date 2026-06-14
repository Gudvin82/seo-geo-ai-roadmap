# Сводка релиза v5.0.0

`v5.0.0` — это релиз про SaaS productization, AI-to-App delivery и executive
operating system.

## Что изменилось

- Добавлена более сильная SaaS box foundation с organization, tenant profile,
  API key, onboarding, role и usage abstractions.
- Добавлены runtime detail views по интеграциям: sync history, freshness,
  readiness, provenance, retry state и recommended next actions.
- Добавлены primitives для proof и attribution: labeled evidence records,
  experiment history, before/after snapshots и confidence labels.
- Добавлены AI-to-App generation contracts, generated project manifests и
  one-link build guidance, чтобы AI agent мог собрать рабочий project shell по
  machine-readable contract.
- Добавлены API-поверхности onboarding-center и operator-center, чтобы
  deployment, setup, troubleshooting и recurring operations были более
  productized.

## Главные продуктовые опоры

- Live integration maturity
- Executive intelligence
- Attribution and evidence
- SaaS box foundation
- AI-to-App delivery mode
- Operator и productization layer
- Bilingual EN и RU product quality

## Новые API-поверхности

- `GET /api/v1/integrations/{integration_id}/detail`
- `GET /api/v1/saas/organizations`
- `POST /api/v1/saas/organizations`
- `GET /api/v1/saas/tenant-profiles`
- `POST /api/v1/saas/tenant-profiles`
- `GET /api/v1/saas/tenant-overview`
- `GET /api/v1/saas/api-keys`
- `POST /api/v1/saas/api-keys`
- `GET /api/v1/proof/labels`
- `GET /api/v1/proof/evidence`
- `POST /api/v1/proof/evidence`
- `GET /api/v1/proof/experiments`
- `POST /api/v1/proof/experiments`
- `GET /api/v1/generation/contracts`
- `POST /api/v1/generation/manifests/generate`
- `GET /api/v1/generation/manifests`
- `GET /api/v1/settings/onboarding-center`
- `GET /api/v1/settings/operator-center`

## Новые операторские entrypoints

- [Build With This Platform](../../BUILD_WITH_THIS_PLATFORM_RU.md)
- [Generate Project From URL](../../GENERATE_PROJECT_FROM_URL_RU.md)

## Честная граница

`v5.0.0` делает репозиторий намного ближе к реальной SaaS foundation, но не
заявляет maintainer-operated hosted SaaS, готовый enterprise billing или
полностью завершенный enterprise SSO из коробки.
