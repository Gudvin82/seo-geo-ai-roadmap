# Сводка релиза v6.4.0

`v6.4.0` усиливает repo от просто сильного foundation до более
operator-ready поверхности для managed runtime, tenant operations, portfolio
review и proof follow-through.

## Что изменилось

- добавлено runtime-policy редактирование для integrations, чтобы ожидания по
  managed runtime были machine-readable и управлялись оператором
- добавлены organization switcher, tenant usage health, quota alerts,
  onboarding checklist и более насыщенный tenant overview
- расширены portfolio dashboards, чтобы оператор мог смотреть один workspace,
  целую organization или все доступные workspace в одном rollup
- добавлен `proof-ops-center` и более богатый proof rendering для evidence,
  experiments, confidence distribution и next recommended steps
- frontend обновлен так, чтобы новые SaaS и proof surfaces были видны как
  cards и operator summaries, а не только как raw JSON
- активные runtime, contract и docs markers выровнены вокруг `v6.4.0`

## Почему это важно

До `v6.4.0` у repo уже был сильный app и API foundation, но managed-runtime
исполнение все еще ощущалось скорее backend-first, чем operator-first.

После `v6.4.0` командам проще:

- понимать, какие integrations действительно готовы к managed-runtime режиму
- видеть usage и onboarding pressure по tenant до того, как это станет support-проблемой
- работать сразу по нескольким workspace или organization из одного portfolio слоя
- вести evidence и experiments как execution loop, а не как статичный proof

## Честная граница

`v6.4.0` все еще **не** означает:

- hosted SaaS от автора репозитория
- полный billing, SSO или zero-touch enterprise onboarding
- что каждая live integration уже полностью plug-and-play в любой среде

Но это означает, что repo стал заметно более операционно цельным для
self-hosted команд, которым нужна не только документация, но и реальная
delivery surface.
