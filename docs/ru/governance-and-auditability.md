# Governance И Auditability

## Текущая auditability boundary

Репозиторий теперь логирует или явно показывает события вокруг:

- provider configuration changes
- audit requests, retries, starts, failures и completions
- workspace role и invite lifecycle actions
- notification endpoint creation и delivery outcomes
- artifact downloads
- governed CMS writeback attempts

## Предположение о governance-модели workspace

`v3.3.0` исходит из trusted workspace administrator model. Это подходит для
self-hosted команд, которым нужна traceability, но это еще не finished
enterprise identity platform.

## Future boundary

В будущем могут появиться:

- SSO
- SCIM
- более сильные approval chains
- durable policy engines

Это direction signals, а не обещание уже реализованной функциональности.
