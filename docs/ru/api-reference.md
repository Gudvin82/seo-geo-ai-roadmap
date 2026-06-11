# API Reference

OpenAPI документация приложения доступна по `/docs`, ReDoc по `/redoc`.

## Health и readiness

- `GET /healthz`
- `GET /readyz`
- `GET /metrics`

## Auth endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`

## Workspace endpoints

- `GET /api/v1/workspaces`
- `POST /api/v1/workspaces`
- `GET /api/v1/workspaces/{workspace_id}`
- `PUT /api/v1/workspaces/{workspace_id}`

## Project endpoints

- `GET /api/v1/projects?workspace_id={workspace_id}`
- `POST /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `GET /api/v1/projects/{project_id}/sites`
- `POST /api/v1/projects/{project_id}/sites`

## Audit endpoints

- `GET /api/v1/audit-runs/presets`
- `GET /api/v1/audit-runs?project_id={project_id}`
- `POST /api/v1/audit-runs`

## Report endpoints

- `GET /api/v1/reports?project_id={project_id}`
- `GET /api/v1/artifacts?project_id={project_id}`
- `GET /api/v1/artifacts/{artifact_id}/download`

## Provider endpoints

- `GET /api/v1/providers?workspace_id={workspace_id}`
- `POST /api/v1/providers`

## Brand facts endpoints

- `GET /api/v1/brand-facts/{project_id}`
- `POST /api/v1/brand-facts`

## Prompt set и scheduled check endpoints

- `GET /api/v1/prompt-sets?workspace_id={workspace_id}`
- `POST /api/v1/prompt-sets`
- `GET /api/v1/scheduled-checks?workspace_id={workspace_id}`
- `POST /api/v1/scheduled-checks`

## Пример request flow

1. Зарегистрировать пользователя.
1. Выполнить login и сохранить bearer token.
1. Создать workspace.
1. Создать project.
1. Добавить brand facts.
1. Запустить audit.
1. Получить reports и artifacts.
