# llms.txt Validator

## Что это такое

В `v3.2.0` добавлен бесплатный validator-asset для `llms.txt`.

Использование:

- API endpoint: `POST /api/v1/tools/llms-validator`
- standalone page: [`app/frontend/llms-validator.html`](../../app/frontend/llms-validator.html)

## Входные режимы

- public URL к `llms.txt`
- вставленный content

## Что на выходе

- сигнал валидности
- warnings
- recommendations
- observed facts по структуре и coverage
