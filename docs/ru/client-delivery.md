# Client Delivery

`v3.1.0` добавляет более сильный delivery-layer для agencies, in-house команд и
founders.

## Аудитории delivery pack

- agency
- in_house
- founder

## One-click deliverables

- audit export
- patch pack
- client delivery pack
- llms.txt improvement suggestions
- starter AI visibility report
- reusable operator-ready JSON payloads

## Текущий API flow

- `GET /api/v1/exports/project-package`
- `POST /api/v1/exports/project-package/import`
- `POST /api/v1/deliverables/patch-pack`
- `POST /api/v1/deliverables/client-pack`

## Что должен включать delivery pack

- delivery summary
- summary по report pack
- summary по artifact pack
- последний SoV summary, если он есть
- audience-aware one-click deliverables для agency, in-house или founder use

## White-label expectations

Клиентская выдача может использовать workspace-branding поля для title,
subtitle, footer и logo placeholder. Но каждый client-facing output всё равно
нужно ревьюить человеком перед отправкой.
