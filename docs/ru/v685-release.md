# Сводка релиза v6.8.5

`v6.8.5` добавляет запланированный community, launch и contributor-growth
layer поверх более сильных docs, proof и operator tooling, введенных в
`v6.7.0`, `v6.7.5` и `v6.8.0`.

## Что изменилось

- добавлены `COMMUNITY_RU.md`, `SHOWCASE_RU.md` и `LAUNCH_PACK_RU.md` как root
  public entrypoints
- добавлены двуязычные community и launch docs внутри `docs/en` и `docs/ru`
- добавлен `scripts/community_showcase_builder.py` для компактного indexing
  proof и showcase materials
- добавлен `scripts/launch_pack_generator.py` для safe public-positioning packs
- добавлены app-level community, participation и launch centers, чтобы этот
  слой был виден в self-hosted product, а не только в markdown

## Почему это важно

До `v6.8.5` у репозитория уже были сильные methodology, proof и operator
tooling. Но public adoption path все еще слишком зависел от того, найдет ли
читатель нужные файлы сам.

После `v6.8.5` командам проще:

- честно объяснять проект публично
- направлять контрибьюторов в правильный intake path
- быстрее показывать самые сильные текущие proof surfaces
- использовать launch-narrative без overclaiming hosted SaaS maturity
