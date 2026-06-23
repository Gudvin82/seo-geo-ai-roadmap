# v6.1.0 Release Summary

`v6.1.0` makes the RU/Yandex GEO layer more real by treating official
`Alice AI visibility` in Yandex Webmaster as a first-class surface.

## What changed

- added `alice_ai_visibility` as a supported integration source
- added starter weekly SoV, query-example, and competitor-overlap payloads
- added `ru_geo_score` to the executive dashboard
- expanded the RU executive layer to review Webmaster, Metrica, Direct, Neuro,
  and Alice AI together
- updated RU and EN methodology docs to reflect Alice AI as an official Yandex
  answer-surface signal

## Why it matters

Before `v6.1.0`, the repo treated RU AI discoverability mainly through:

- `YandexAdditional`
- `Yandex Neuro readiness`
- answer-ready RU content

After `v6.1.0`, the product can also express:

- official Alice AI share-of-voice framing
- insufficient-data diagnosis
- query/page/source-example review
- a clearer RU GEO operating score

## What this still does not claim

- direct control over Alice AI answers
- guaranteed inclusion in Yandex AI answers
- a finished public SaaS around Yandex APIs

It remains a self-hosted execution system with honest operator guidance.
