# Журнал изменений

Русскоязычная сводка последних релизов.

## v4.5.0 — Чистый test path, production-flows интеграций, onboarding без трения

- Корневой test path переведен в полностью зеленое состояние без оговорок и без предупреждений
- Scanner получил более сильные публичные runtime-контроли: queue visibility, per-IP window rate limit, per-domain concurrency guard и retryable notifications
- Integration layer усилен через более явный env-aware verification matrix для GSC, GA4, Yandex и CrUX
- Provider surface расширен до более широкого online и local каталога, чтобы self-hosted и hybrid сценарии были проще
- Добавлены новые EN/RU entrypoints для onboarding за 15 минут, docs consolidation, provider catalog и integration production matrix

## История

Полная каноническая история релизов ведется в [CHANGELOG.md](./CHANGELOG.md).
