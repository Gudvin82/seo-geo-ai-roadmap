# v4.5.0 Release Summary

`v4.5.0` is the release that cleans up the operator path and removes the last
"yes, but..." around root testing and onboarding.

## What materially changed

- root and backend tests now pass together from the repository root without
  caveats
- scanner runtime now exposes stronger queue and anti-abuse controls
- integration verification is more production-shaped through environment-aware
  readiness reporting
- provider coverage is much wider for hosted and local deployment patterns
- documentation now has explicit current entrypoints so newcomers do not need
  to reverse-engineer the repo history

## Scanner upgrades

- per-IP submission window limits
- per-domain concurrency limits
- global pending queue ceiling
- queue depth and queue position visibility
- notification retries for webhook, email, and Telegram delivery paths

## RU market depth

- `YandexAdditional` remains a first-class surface, separate from `YandexBot`
- RU operator flows now sit more clearly next to Yandex Webmaster and Yandex
  Metrica production paths
- public RU case evidence already present in the repository remains part of the
  current release story

## New entrypoints

- [DOCS_INDEX.md](../../DOCS_INDEX.md)
- [docs/en/15-minute-onboarding-v450.md](./15-minute-onboarding-v450.md)
- [docs/en/integration-production-matrix-v450.md](./integration-production-matrix-v450.md)
- [docs/en/provider-catalog-v450.md](./provider-catalog-v450.md)
