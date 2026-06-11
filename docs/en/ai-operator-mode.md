# AI Operator Mode

This platform is designed so a human operator or AI coding agent can adapt it to a real site.

## Typical operator loop

1. Deploy the platform locally or in self-hosted mode.
1. Connect cloud providers or local LLM endpoints such as Ollama or LocalAI.
1. Open `/docs`, `/redoc`, and the frontend UI.
1. Create a workspace and project for the target site.
1. Add brand facts, provider settings, and team roles if needed.
1. Run a canonical audit job through `POST /api/v1/audit-runs/run`.
1. Review artifacts, findings, reports, and audit logs.
1. Turn findings into implementation tasks or patch artifacts.
1. Re-run after fixes and compare outputs.

## What an AI coding agent can do

- run checks through the API
- inspect reports and artifacts
- compare outputs with docs and checklists
- generate `llms.txt` and related AI files
- update brand facts and truth-center content
- draft implementation tasks and release notes

## Adapt-my-site playbooks

- Local business site
- Service company site
- Expert / personal brand site
- SaaS / product site
- Multilingual site
- Agency client onboarding

Use the repo methodology and the app layer together. The platform is not a black box.
