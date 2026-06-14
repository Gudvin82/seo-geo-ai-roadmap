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

## Search and analytics integrations

- `GET /api/v1/integrations?project_id={project_id}`
- `POST /api/v1/integrations`
- `POST /api/v1/integrations/{integration_id}/sync`

Starter source values:

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

## CMS connectors and patch package flow

- `GET /api/v1/cms?project_id={project_id}`
- `POST /api/v1/cms`
- `POST /api/v1/cms/{connector_id}/inventory`
- `POST /api/v1/cms/{connector_id}/patch-package`
- `GET /api/v1/integrations/verification-matrix?project_id={project_id}`

Writeback modes:

- `read_only`
- `draft`
- `human_approved_publish`

## Deliverables

- `POST /api/v1/deliverables/patch-pack`
- `POST /api/v1/deliverables/client-pack`

Audience values:

- `agency`
- `in_house`
- `founder`

Deliverables return structured outputs such as issue backlog items,
developer-ready briefs, content briefs, schema suggestions, and client delivery
summaries.

## Export and import package

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

Example payload:

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

Or:

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

Scanner requests are session-bound through the `X-Scanner-Session` header.
Active and full scans require ownership verification plus consent.

From `v3.7.0`, scanner artifacts and summaries may also include module-level
results for:

- RU and AI bot policy, including `YandexAdditional`
- `ai.txt`
- schema coverage
- FAQ / answer-ready detection
- Open Graph / Twitter Card completeness
- `robots.txt` ↔ sitemap linkage

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
