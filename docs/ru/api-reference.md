# API Reference

OpenAPI доступен по `/docs`, ReDoc по `/redoc`.

## Auth

Авторизация работает через `Authorization: Bearer <token>`.

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
- `GET /api/v1/workspaces/{workspace_id}/invites`
- `POST /api/v1/workspaces/{workspace_id}/invites`
- `POST /api/v1/workspaces/invites/accept`

Правила workspace isolation:

- viewers могут читать
- editors могут создавать project и audit content
- admins могут управлять provider configs и invites
- owners сохраняют полный governance-контроль

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

### Жизненный цикл audit job

Поддерживаемые состояния:

- `queued`
- `running`
- `partial`
- `completed`
- `failed`
- `canceled`

В текущей реализации активно используются `queued`, `running`, `completed` и
`failed`.

### Audit status

- `GET /api/v1/audit-runs/{audit_run_id}`
- `GET /api/v1/audit-runs?project_id={project_id}`
- `GET /api/v1/audit-runs/presets`

## Reports и artifacts

- `GET /api/v1/reports?project_id={project_id}`
- `GET /api/v1/artifacts?project_id={project_id}`
- `GET /api/v1/artifacts/{artifact_id}/download`

Artifact download требует workspace access и возвращает сохраненный файл
напрямую.

## Providers

- `GET /api/v1/providers?workspace_id={workspace_id}`
- `POST /api/v1/providers`

Пример local provider config:

```json
{
  "workspace_id": 1,
  "provider_name": "ollama",
  "label": "Local Ollama",
  "model": "llama3.1",
  "base_url": "http://ollama:11434/v1/chat/completions"
}
```

## Brand facts

- `GET /api/v1/brand-facts/{project_id}`
- `POST /api/v1/brand-facts`

## Audit logs

- `GET /api/v1/audit-logs?workspace_id={workspace_id}`

## Error model

- `401`: отсутствует токен или истек срок жизни
- `403`: роли недостаточно
- `404`: ресурс не найден в рамках текущего workspace boundary
- `422`: payload validation failed
- `429`: сработал login rate limit
