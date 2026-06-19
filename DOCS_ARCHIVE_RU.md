# Политика архива документации

В репозитории накопилось много release- и version-specific документов из эпох
`v3.x`, `v4.x` и `v5.x`.

Это полезная история, но ее не надо путать с кратчайшим путем для нового
читателя.

## Актуальные entrypoints

Сначала идите сюда:

1. [README_RU.md](./README_RU.md)
2. [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
3. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
4. [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
5. [REAL_CASES_RU.md](./REAL_CASES_RU.md)
6. [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
7. [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)

## Что считается архивным материалом

Эти документы полезны, но не должны быть первой точкой входа:

- `docs/en/*-vXYZ.md`
- `docs/ru/*-vXYZ.md`
- исторические release summaries
- version-specific rollout notes
- промежуточные документы с ответами на reviews и upgrade-path

## Зачем вообще хранить архив

- он сохраняет эволюцию продукта
- показывает честную реакцию на критику и сбои
- помогает понять, почему в проекте появились те или иные границы
- делает публичные claims аудируемыми

## Как правильно его читать

Архив нужен, когда вам важны:

- хронология релизов
- историческая логика решений
- доказательство, когда именно feature вошла в repo
- сравнение старой и текущей позиции проекта

Не используйте архив как первое объяснение проекта.

## Правило v6

Начиная с `v6.0.0`:

- root entrypoints объясняют текущий продукт
- archive files остаются для evidence и истории
- README должен сначала вести в current docs, а не в historical slices
