# Сводка релиза v4.5.0

`v4.5.0` — это релиз, который дочищает операторский путь и снимает последнее
"да, но..." вокруг корневого тестирования и onboarding.

## Что изменилось по сути

- root и backend tests теперь проходят вместе от корня репозитория без
  оговорок
- scanner runtime получил более сильные queue и anti-abuse controls
- integration verification стал ближе к production через environment-aware
  readiness reporting
- provider coverage заметно шире для hosted и local deployment patterns
- документация получила явные актуальные entrypoints, чтобы новичок не
  распутывал историю релизов вручную

## Улучшения scanner

- per-IP submission window limits
- per-domain concurrency limits
- global pending queue ceiling
- видимость queue depth и queue position
- retry-модель для webhook, email и Telegram notification paths

## Глубина по RU рынку

- `YandexAdditional` остается first-class surface отдельно от `YandexBot`
- RU operator flows теперь яснее стоят рядом с production paths для Yandex
  Webmaster и Yandex Metrica
- публичные RU-кейсы, уже лежащие в репозитории, остаются частью актуальной
  release-story

## Новые entrypoints

- [DOCS_INDEX_RU.md](../../DOCS_INDEX_RU.md)
- [docs/ru/15-minute-onboarding-v450.md](./15-minute-onboarding-v450.md)
- [docs/ru/integration-production-matrix-v450.md](./integration-production-matrix-v450.md)
- [docs/ru/provider-catalog-v450.md](./provider-catalog-v450.md)
