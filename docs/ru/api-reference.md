# API Reference

OpenAPI доступен по `/docs`, ReDoc по `/redoc`.

## Auth

Используйте `Authorization: Bearer <token>`.

### Register

`POST /api/v1/auth/register`

```json
{
  "email": "operator@example.com",
  "password": "StrongPass123"
}
```

### Login

`POST /api/v1/auth/login`

Возвращает `access_token`, `expires_at` и `expires_in_seconds`.

## Workspaces, roles и invites

- `GET /api/v1/workspaces`
- `POST /api/v1/workspaces`
- `GET /api/v1/workspaces/{workspace_id}`
- `PUT /api/v1/workspaces/{workspace_id}`
- `GET /api/v1/workspaces/{workspace_id}/members`
- `PUT /api/v1/workspaces/{workspace_id}/members/{member_id}`
- `GET /api/v1/workspaces/{workspace_id}/invites`
- `POST /api/v1/workspaces/{workspace_id}/invites`
- `PUT /api/v1/workspaces/{workspace_id}/invites/{invite_id}`
- `POST /api/v1/workspaces/{workspace_id}/invites/{invite_id}/resend`
- `POST /api/v1/workspaces/{workspace_id}/invites/{invite_id}/revoke`
- `POST /api/v1/workspaces/invites/accept`

Правила isolation:

- `viewer`: читает projects, reports и artifacts
- `editor`: создает projects, facts, audits и SoV-проверки
- `admin`: управляет invites, providers и более широкими workspace-операциями
- `owner`: полный governance, role changes и ownership-sensitive actions

## Projects и sites

- `GET /api/v1/projects?workspace_id={workspace_id}`
- `POST /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `GET /api/v1/projects/{project_id}/sites`
- `POST /api/v1/projects/{project_id}/sites`

## Canonical audit execution

### Запуск аудита

`POST /api/v1/audit-runs/run`

```json
{
  "workspace_id": 1,
  "project_id": 1,
  "domain_or_url": "https://example.com",
  "selected_checks": ["factual_consistency", "llms_txt"],
  "selected_providers": ["ollama"],
  "report_language": "ru",
  "market": "RU",
  "mode": "quick"
}
```

Ответ:

```json
{
  "audit_job_id": 12,
  "initial_status": "queued",
  "accepted_parameters": {},
  "status_endpoint": "/api/v1/audit-runs/12",
  "report_endpoint": "/api/v1/reports?project_id=1",
  "artifacts_endpoint": "/api/v1/artifacts?project_id=1"
}
```

### Жизненный цикл аудита

Поддерживаемые статусы:

- `queued`
- `running`
- `partial`
- `completed`
- `failed`
- `canceled`

Текущая реализация активно использует `queued`, `running`, `completed` и
`failed`.

### Audit status и retry

- `GET /api/v1/audit-runs/{audit_run_id}`
- `GET /api/v1/audit-runs?project_id={project_id}`
- `GET /api/v1/audit-runs/presets`
- `POST /api/v1/audit-runs/{audit_run_id}/retry`

В `v3.0.0` findings в отчетах теперь содержат:

- `impact`
- `effort`
- `confidence`
- `priority_score`
- `priority_label`
- `benchmark_status`

## Reports и artifacts

- `GET /api/v1/reports?project_id={project_id}`
- `GET /api/v1/artifacts?project_id={project_id}`
- `GET /api/v1/artifacts/{artifact_id}/download`

Артефакты и отчеты могут содержать:

- benchmark summary
- AI Citation Score
- двуязычный markdown report
- JSON payload для дальнейшей автоматизации

## Providers

- `GET /api/v1/providers?workspace_id={workspace_id}`
- `POST /api/v1/providers`
- `PUT /api/v1/providers/{provider_id}`

Пример provider config:

```json
{
  "workspace_id": 1,
  "provider_name": "openai",
  "label": "Primary OpenAI",
  "model": "gpt-4.1-mini",
  "api_key_env_var": "OPENAI_API_KEY",
  "base_url": null,
  "is_enabled": true
}
```

## Brand facts

- `GET /api/v1/brand-facts/{project_id}`
- `POST /api/v1/brand-facts`

Это главный вход в подсистему factual consistency для canonical brand, numeric,
market и language claims.

## AI Share of Voice

- `POST /api/v1/sov/check`
- `GET /api/v1/sov/history?project_id={project_id}`
- `GET /api/v1/sov/{sov_run_id}`

Заметки по AI SoV:

- provider-backed execution используется, когда есть совпадающий enabled
  provider config
- иначе используется heuristic fallback
- AI Citation Score считается из структурированных результатов и пишется в
  summary и audit logs
- AI answer surfaces остаются волатильными и требуют human review

## Notifications

- `GET /api/v1/notifications?workspace_id={workspace_id}`
- `POST /api/v1/notifications`

## Search и analytics integrations

- `GET /api/v1/integrations?project_id={project_id}`
- `POST /api/v1/integrations`
- `POST /api/v1/integrations/{integration_id}/sync`

Допустимые starter source values:

- `gsc`
- `ga4`
- `google_ads`
- `yandex_webmaster`
- `yandex_metrica`
- `yandex_direct`
- `crux`
- `indexnow`
- `google_business_profile`
- `yandex_business`
- `merchant_center`
- `meta_ads`
- `x_ads`
- `x_organic`
- `threads`
- `reddit_mentions`
- `tiktok_organic`
- `vk_ads`
- `telegram_ads`
- `youtube`
- `linkedin_ads`
- `instagram_facebook_organic`

## CMS connectors и patch-package flow

- `GET /api/v1/cms?project_id={project_id}`
- `POST /api/v1/cms`
- `POST /api/v1/cms/{connector_id}/inventory`
- `POST /api/v1/cms/{connector_id}/patch-package`
- `GET /api/v1/integrations/verification-matrix?project_id={project_id}`

Режимы writeback:

- `read_only`
- `draft`
- `human_approved_publish`

## Deliverables

- `POST /api/v1/deliverables/patch-pack`
- `POST /api/v1/deliverables/client-pack`

Допустимые audience values:

- `agency`
- `in_house`
- `founder`

Deliverables возвращают структурированные outputs: issue backlog items,
developer-ready briefs, content briefs, schema suggestions и client delivery
summaries.

## Export и import package

- `GET /api/v1/exports/project-package?project_id={project_id}`
- `POST /api/v1/exports/project-package/import`

## Operator settings helpers

- `GET /api/v1/settings/repo-assets`
- `GET /api/v1/settings/prompt-library`
- `GET /api/v1/settings/integration-starters`
- `GET /api/v1/settings/vertical-packs`
- `GET /api/v1/settings/review-mode`
- `GET /api/v1/settings/social-distribution-center`
- `GET /api/v1/settings/social-intelligence-center?project_id={project_id}`
- `GET /api/v1/settings/saas-growth-center?workspace_id={workspace_id}`
- `GET /api/v1/settings/repo-understanding-center`
- `GET /api/v1/settings/deploy-wizard`

## Tools

- `GET /api/v1/tools/command-catalog`
- `POST /api/v1/tools/command-router`
- `POST /api/v1/tools/llms-validator`
- `POST /api/v1/tools/fact-drift`

Пример payload:

```json
{
  "url": "https://example.com/llms.txt"
}
```

Command router payload:

```json
{
  "command": "audit"
}
```

Или:

```json
{
  "content": "# Example llms.txt\n- Home: https://example.com/\n- FAQ: https://example.com/faq"
}
```

## Public scanner foundation

- `GET /api/v1/scanner/config`
- `POST /api/v1/scanner/verification-requests`
- `POST /api/v1/scanner/verification-requests/{id}/verify`
- `POST /api/v1/scanner/consent-records`
- `POST /api/v1/scan-jobs`
- `GET /api/v1/scan-jobs/{id}`
- `POST /api/v1/scan-jobs/{id}/cancel`
- `GET /api/v1/scan-jobs/{id}/events`
- `GET /api/v1/scan-jobs/{id}/artifacts`
- `GET /api/v1/scan-jobs/{id}/artifacts/{filename}`

Scanner requests привязаны к `X-Scanner-Session` header.
Active и full scan modes требуют ownership verification и consent.

Начиная с `v3.7.0`, scanner artifacts и summary также могут включать
module-level results для:

- RU и AI bot policy, включая `YandexAdditional`
- `ai.txt`
- schema coverage
- FAQ / answer-ready detection
- полноты Open Graph / Twitter Card
- связки `robots.txt` ↔ sitemap

## Audit logs

- `GET /api/v1/audit-logs?workspace_id={workspace_id}`

Audit logs теперь включают:

- login и auth activity
- provider changes
- audit requests и retries
- SoV completion
- invite acceptance
- role changes

## Error model

- `401`: отсутствует токен или истек срок жизни
- `403`: роли недостаточно для ресурса или действия
- `404`: ресурс не найден в пределах текущей workspace boundary
- `422`: payload validation failed
- `429`: сработал rate limit на чувствительном сценарии, например login
