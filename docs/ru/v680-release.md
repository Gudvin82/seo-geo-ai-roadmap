# Сводка релиза v6.8.0

`v6.8.0` усиливает proof, case и working-tool layer репозитория.

## Что изменилось

- добавлен `scripts/case_library_builder.py`
- добавлен `scripts/synthetic_case_builder.py`
- добавлен `scripts/issue_pack_generator.py`
- расширены case и proof docs через synthetic-case и issue-pack workflows
- расширены proof kit и evidence lab surfaces через более сильные сигналы
  case-library и export readiness
- добавлены более сильные issue templates и richer proof/case templates

## Почему это важно

До `v6.8.0` у репозитория уже были bounded public cases и сильные proof
primitives, но repeatable tooling вокруг них все еще отставал от самой
методологии.

После `v6.8.0` командам проще:

- тренироваться на synthetic, но явно маркированных cases
- строить case library index
- переводить findings в issue packs для implementation teams
- держать proof, cases и exports более структурированными и повторяемыми
