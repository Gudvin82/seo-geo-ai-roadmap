# Операционные Повторы

## Какие повторы есть в `v3.3.0`

Платформа теперь показывает стартовую retry-модель для:

- provider-backed комментариев и provider-вызовов в AI SoV
- доставки webhook и уведомлений
- подготовки governed CMS writeback

Цель не в том, чтобы притворяться durable job orchestrator. Цель в том, чтобы
ошибки были видимыми, ограниченными и пригодными для ревью.

## Политика повторов

- максимум попыток: `3`
- начальная задержка: `0.5s`
- модель backoff: bounded exponential (`0.5s`, `1.0s`, `2.0s`)
- терминальное состояние: `dead`

## Статусы

- `queued`: задача принята, но еще не выполнена
- `retrying`: одна или несколько попыток уже упали, система пробует снова
- `failed`: текущая попытка неуспешна, но терминальное состояние еще не достигнуто
- `dead`: лимит попыток исчерпан, нужен человек
- `completed`: выполнение завершилось успешно
- `awaiting_human_approval`: governed CMS package готов, но live publish заблокирован

## Когда нужен человек

Human review обязателен, если:

- неверные или отсутствующие provider credentials
- webhook target недоступен или стабильно возвращает ошибки
- для CMS writeback нет свежего audit run
- CMS connector работает в режиме `read_only`

## Текущая граница

`v3.3.0` не обещает durable queue или exactly-once execution. Повторы здесь —
это process-level safeguard и auditability, а не полноценный workflow engine.
