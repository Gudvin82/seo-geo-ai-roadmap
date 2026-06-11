# API Reference

OpenAPI is available at `/docs` and ReDoc at `/redoc`.

## Auth

Auth uses `Authorization: Bearer <token>`.

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

Returns `access_token`, `expires_at`, and `expires_in_seconds`.

## Workspaces, roles, and invites

- `GET /api/v1/workspaces`
- `POST /api/v1/workspaces`
- `GET /api/v1/workspaces/{workspace_id}`
- `PUT /api/v1/workspaces/{workspace_id}`
- `GET /api/v1/workspaces/{workspace_id}/members`
- `GET /api/v1/workspaces/{workspace_id}/invites`
- `POST /api/v1/workspaces/{workspace_id}/invites`
- `POST /api/v1/workspaces/invites/accept`

Workspace isolation rules:

- viewers can read
- editors can create project and audit content
- admins can manage provider configs and invites
- owners keep full governance

## Projects and sites

- `GET /api/v1/projects?workspace_id={workspace_id}`
- `POST /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `GET /api/v1/projects/{project_id}/sites`
- `POST /api/v1/projects/{project_id}/sites`

## Canonical audit execution

### Launch an audit

`POST /api/v1/audit-runs/run`

```json
{
  "workspace_id": 1,
  "project_id": 1,
  "domain_or_url": "https://example.com",
  "selected_checks": ["factual_consistency", "llms_txt"],
  "selected_providers": ["ollama"],
  "report_language": "en",
  "market": "Global",
  "mode": "quick"
}
```

Response:

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

### Audit lifecycle

Supported states:

- `queued`
- `running`
- `partial`
- `completed`
- `failed`
- `canceled`

Current implementation actively uses `queued`, `running`, `completed`, and
`failed`.

### Audit status

- `GET /api/v1/audit-runs/{audit_run_id}`
- `GET /api/v1/audit-runs?project_id={project_id}`
- `GET /api/v1/audit-runs/presets`

## Reports and artifacts

- `GET /api/v1/reports?project_id={project_id}`
- `GET /api/v1/artifacts?project_id={project_id}`
- `GET /api/v1/artifacts/{artifact_id}/download`

Artifact downloads require workspace access and return the stored file directly.

## Providers

- `GET /api/v1/providers?workspace_id={workspace_id}`
- `POST /api/v1/providers`

Example local provider config:

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

- `401`: missing or expired token
- `403`: role is insufficient
- `404`: resource not found within the current workspace boundary
- `422`: payload validation failed
- `429`: login rate limit triggered
