# Сводка релиза v6.7.5

`v6.7.5` двигает репозиторий еще ближе к сильному operator toolkit, а не только
к методологической карте.

## Что изменилось

- добавлен `scripts/checklist_generator.py` для tailored SEO/GEO/AI checklists
- добавлен `scripts/semantic_gap_mapper.py` для keyword clustering и
  page-type planning
- добавлен `scripts/proof_pack_builder.py` для bounded before/after evidence
  packs
- добавлены новые EN/RU docs для checklist generator, proof-pack flow и
  case-library entrypoint
- расширен command surface, чтобы агенты явнее маршрутизировали semantic и
  proof-pack задачи

## Почему это важно

До `v6.7.5` у репозитория уже были сильные docs и широкий command surface, но
часть критики была справедливой: оператору все еще приходилось слишком много
собирать вручную, когда методологию нужно было превратить в execution.

После `v6.7.5` командам проще:

- сгенерировать tailored starting checklist
- превратить набор keyword в semantic execution lanes
- упаковать proof в reusable public или client-safe формат

## Что все еще верно

`v6.7.5` все еще **не** означает:

- что у репозитория уже есть большой независимый benchmark corpus
- что весь public case evidence автоматизирован end-to-end
- что classical SEO depth уже может заменить specialist judgment
