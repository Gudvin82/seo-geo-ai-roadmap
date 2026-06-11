# Граница Open-Source и SaaS

## Что остается open-source

Методологический слой репозитория полностью остается открытым и переиспользуемым:

- docs
- checklists
- prompts
- templates
- scripts
- examples
- docs-site

## Что добавляет app layer

`v2.0.0` добавляет разворачиваемый foundation продукта:

- авторизацию
- workspaces и projects
- структурированные audit runs
- хранение evidence
- генерацию EN/RU отчетов
- конфигурацию провайдеров
- self-hosted deployment foundation

## Как работает self-hosting

App layer можно развернуть через:

- локальный backend с SQLite
- Docker Compose
- контейнерный стек с PostgreSQL

Репозиторий спроектирован так, чтобы self-hosting не зависел от будущего managed SaaS.

## Что может появиться в будущем managed SaaS

- billing
- управляемый командный доступ
- более сильная tenancy-модель
- hosted analytics
- масштабируемый job scheduling
- managed reliability и support

## Что еще не реализовано в v2.0.0

- billing и payments
- enterprise SSO
- сложная permissions matrix
- usage metering
- analytics warehouse
- production SLA

Цель здесь — доверие: честно зафиксировать границу, а не делать вид, что этих
возможностей уже достаточно.
