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

`v2.2.0` добавляет operator-ready foundation продукта:

- авторизацию
- workspaces и projects
- структурированные audit runs
- хранение evidence
- генерацию EN/RU отчетов
- конфигурацию провайдеров
- self-hosted deployment foundation
- expiring auth tokens и более сильную работу с паролями
- migrations, demo seed data и базовую observability
- workspace roles, invites, audit logs и canonical audit API
- local LLM support для Ollama, LocalAI и vLLM-style endpoints

## Явное обещание платформы

Эта платформа:

- бесплатная
- прозрачная
- self-hosted first
- совместима с вашими cloud AI providers и local LLM runtimes
- exportable by design

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
