# Review Mode

Review mode объясняет, что платформа может автоматизировать, что требует
approval и что нельзя auto-apply.

## Можно автоматизировать

- inventory sync
- starter data import
- artifact generation
- draft patch packs
- сборку exportable client packs

## Требует human review

- переписывание titles
- изменения schema
- public-facing claims
- white-label framing
- human-approved publish
- формулировки клиентской выдачи

## Нельзя auto-apply

- silent destructive changes
- publish без review
- legal или safety-sensitive claims без approval

## Предполагаемая операторская позиция

Этот режим нужен, чтобы и люди, и AI-агенты понимали границу approval. В
`v3.1.0` стало больше operational output, но это не отменяет review перед
publication, client delivery и чувствительными factual claims.
