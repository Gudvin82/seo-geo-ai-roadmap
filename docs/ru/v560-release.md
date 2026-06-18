# Сводка релиза v5.6.0

`v5.6.0` усиливает проект от сильной self-hosted SaaS-ready основы до более
production-похожей операторской системы для интеграций, RU market execution и
social-commerce intelligence.

## Что изменилось

- Добавлены integration runtime profiles, чтобы по каждой интеграции было видно:
  cadence обновления, retry policy, ожидания по token rotation, runtime level и
  recovery guidance.
- Добавлен отдельный integration runtime center в API и во frontend.
- Существенно усилен RU market слой:
  `yandex_neuro`, `vk_organic`, `telegram_channels`, `dzen`, `rutube`.
- Добавлен отдельный RU market command center, который объединяет:
  Yandex search, Yandex local, RU AI readiness, RU social distribution и local
  trust overlays.
- Расширены social и commercial operator loops, чтобы community demand можно
  было превращать в:
  FAQ blocks, trust blocks, proof strips, objection handling и sales-ready
  messaging assets.
- Яснее зафиксировано, что проект остается бесплатным и self-hosted по
  умолчанию, поэтому billing не является обязательной частью обещания для
  операторских инсталляций.

## Почему это важно

Этот релиз делает репозиторий полезнее для агентств, фаундеров и in-house
команд, которым нужна не только методология:

- видно, какие интеграции все еще starter-level,
- какие уже ближе к managed runtime поведению,
- как интерпретировать RU demand и local trust,
- и как social signals превращать в реальные deliverables и коммерческий
  контент.

## Честная граница

`v5.6.0` все еще **не** означает:

- maintainer-hosted public SaaS,
- обязательный billing или подписки,
- enterprise SSO или SCIM из коробки,
- полностью автономный no-review publishing.

Но означает более сильный self-hosted и operator-controlled product layer,
который гораздо ближе к реальной регулярной работе.
