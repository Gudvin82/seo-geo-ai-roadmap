# API Reference

OpenAPI is available at `/docs` and ReDoc at `/redoc`.

## Auth

Use `Authorization: Bearer <token>`.

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
- `PUT /api/v1/workspaces/{workspace_id}/members/{member_id}`
- `GET /api/v1/workspaces/{workspace_id}/invites`
- `POST /api/v1/workspaces/{workspace_id}/invites`
- `PUT /api/v1/workspaces/{workspace_id}/invites/{invite_id}`
- `POST /api/v1/workspaces/{workspace_id}/invites/{invite_id}/resend`
- `POST /api/v1/workspaces/{workspace_id}/invites/{invite_id}/revoke`
- `POST /api/v1/workspaces/invites/accept`

Isolation rules:

- `viewer`: read projects, reports, and artifacts
- `editor`: create projects, facts, audits, and SoV checks
- `admin`: manage invites, providers, and broader workspace operations
- `owner`: full governance, role changes, and ownership-sensitive actions

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

### Audit status and retry

- `GET /api/v1/audit-runs/{audit_run_id}`
- `GET /api/v1/audit-runs?project_id={project_id}`
- `GET /api/v1/audit-runs/presets`
- `POST /api/v1/audit-runs/{audit_run_id}/retry`

`v3.0.0` reports now surface benchmark-aware findings with:

- `impact`
- `effort`
- `confidence`
- `priority_score`
- `priority_label`
- `benchmark_status`

## Reports and artifacts

- `GET /api/v1/reports?project_id={project_id}`
- `GET /api/v1/artifacts?project_id={project_id}`
- `GET /api/v1/artifacts/{artifact_id}/download`

Artifacts and reports may include:

- benchmark summary
- AI Citation Score
- bilingual markdown report output
- JSON payload for downstream automation

## Providers

- `GET /api/v1/providers?workspace_id={workspace_id}`
- `POST /api/v1/providers`
- `PUT /api/v1/providers/{provider_id}`

Example provider config:

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

This is the factual consistency subsystem entrypoint for canonical brand,
numeric, market, and language claims.

## AI Share of Voice

- `POST /api/v1/sov/check`
- `GET /api/v1/sov/history?project_id={project_id}`
- `GET /api/v1/sov/{sov_run_id}`

AI SoV notes:

- provider-backed execution is used when a matching enabled provider config
  exists
- heuristic fallback is used otherwise
- AI Citation Score is derived from structured results and stored in summary
  text and audit logs
- AI answer surfaces remain volatile and require human review

## Notifications

- `GET /api/v1/notifications?workspace_id={workspace_id}`
- `POST /api/v1/notifications`

## Export package

- `GET /api/v1/exports/project-package?project_id={project_id}`

## Audit logs

- `GET /api/v1/audit-logs?workspace_id={workspace_id}`

Audit logs now include entries for:

- login and auth activity
- provider changes
- audit requests and retries
- SoV completion
- invite acceptance
- role changes

## Error model

- `401`: missing or expired token
- `403`: insufficient role for the resource or action
- `404`: resource not found inside the current workspace boundary
- `422`: payload validation failed
- `429`: rate limit triggered on sensitive flows such as login
