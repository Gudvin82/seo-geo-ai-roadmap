# Сводка релиза v6.6.0

`v6.6.0` закрывает еще один разрыв между сильной self-hosted foundation и более
чистой operator-ready платформой за счет tenant admin visibility,
managed-integration proof и более строгой release hygiene.

## Что изменилось

- добавлен `tenant-admin-console`, чтобы оператор мог видеть tenant profiles,
  plan posture, quota pressure, onboarding state и API key counts в одной
  поверхности
- добавлен `managed-integration-center`, чтобы GSC, GA4, Google Ads, Yandex
  Webmaster, Yandex Metrica, Yandex Direct, local business surfaces, Alice AI
  и CrUX были собраны в одну machine-readable production-flow матрицу
- добавлен `docs-consolidation-center`, который явно показывает current doc
  path, AI-agent path, service-builder path и archive policy прямо внутри
  продуктового слоя
- новые admin, docs и managed-integration центры выведены во frontend, а не
  оставлены backend-only
- добавлен `release-hygiene` CI, который проверяет version markers, release
  docs, docs build и frontend syntax как единый release discipline path

## Почему это важно

До `v6.6.0` repo уже имел более сильные runtime ops, SEO maturity и evidence
surfaces, но часть service-builder и release-governance слоев все еще была
скорее подразумеваемой, чем по-настоящему productized.

После `v6.6.0` командам проще:

- управлять несколькими tenant profiles с более явной видимостью квот и
  onboarding
- понимать, какие integrations все еще starter-first, какие уже live-runtime,
  а какие ближе к managed-runtime discipline
- вести новых пользователей по более чистому current-docs path без repo
  archaeology
- уменьшать version drift между backend, frontend и публичными docs

## Честная граница

`v6.6.0` все еще **не** означает:

- hosted SaaS от автора
- billing и subscription maturity
- zero-touch внешние integrations в любой среде

Но это означает, что бесплатная self-hosted платформа стала честнее,
наблюдаемее и удобнее как multi-tenant operator system.
