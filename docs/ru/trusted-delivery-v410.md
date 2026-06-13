# Trusted Delivery Targets v4.1.0

В `v4.1.0` появился governed trusted-delivery слой для репозиториев, где PR
может готовиться под low-friction merge flow.

## Что добавлено

- `POST /api/v1/trusted-delivery-targets`
- `GET /api/v1/trusted-delivery-targets`
- `POST /api/v1/deliverables/pr-proposal`

## Зачем это нужно

Это переводит репозиторий от абстрактных "PR-ready payloads" к явному
контракту для trusted repositories, required checks и auto-merge eligibility.

## Важная граница

Система теперь умеет собирать PR proposal c:

- repository
- base branch
- branch name
- issue backlog
- required checks
- auto-merge eligibility flag

Сам merge по-прежнему зависит от repository policy, credentials и CI.
