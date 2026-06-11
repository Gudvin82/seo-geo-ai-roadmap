# Observability and Logging

## Встроенная видимость

- `/healthz` для базового health
- `/readyz` для readiness
- `/metrics` для Prometheus-style counters

## Что считается

- auth requests
- audit runs
- provider calls
- provider failures
- report generation events

## Базовый debugging

- смотрите backend logs для request failures
- проверяйте artifact outputs для audit-specific issues
- проверяйте provider metadata в report artifacts при missing-key и timeout ошибках
