# Patch Mode

Patch mode в `v3.1.0` переводит платформу из режима "нашли проблему" в режим
"подготовили implementation work".

## Типы outputs

- issue-ready backlog items
- developer-ready implementation briefs
- content briefs
- schema patch suggestions
- llms.txt и AI visibility suggestions
- client-safe patch pack artifacts

## Review stance

- outputs создаются как явные artifacts
- review mode всегда виден
- CMS writeback регулируется режимами `read_only`, `draft` или
  `human_approved_publish`

## Текущий API flow

- `POST /api/v1/deliverables/patch-pack`
- `POST /api/v1/cms/{connector_id}/patch-package`
