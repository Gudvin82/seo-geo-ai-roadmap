# CMS Connectors

`v3.1.0` делает CMS connectors более операционными и явно фиксирует безопасные
границы writeback.

## Поддерживаемые connectors

- WordPress
- Tilda
- Bitrix
- Webflow

## Текущий полезный scope

- создать connector на каждый project
- синхронизировать inventory
- маппить titles, slugs, status, URL и metadata fields
- генерировать governed patch packages
- экспортировать suggested changes для человека или AI-агента

## Режимы writeback

- `read_only`
- `draft`
- `human_approved_publish`

## Безопасные границы

Безопасно:

- inventory content
- mapping metadata/title/status
- patch suggestions
- schema и llms.txt suggestions
- exportable implementation payloads

Требует human review:

- переписывание titles
- изменения schema
- publish operations
- изменения клиентских формулировок

Не поддерживается:

- silent destructive updates
- автоматический publish без review

## WordPress notes

WordPress starter connector сейчас самый полезный путь в релизе. Он рассчитан
на page fetching, metadata mapping и exportable suggested changes до любого
шага publish.

## RU-market notes

Tilda и Bitrix стратегически важны для RU-market operator flows. В `v3.1.0`
они документированы как starter connectors с inventory и governed patch package
support.
