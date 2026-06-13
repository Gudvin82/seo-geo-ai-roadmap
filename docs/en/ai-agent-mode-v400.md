# AI Agent Mode v4.0.0

`v4.0.0` adds a real agent-mode layer above scripts and manual commands.

Supported modes:

- `manual`
- `scheduled`
- `watch`
- `agent-review`
- `agent-plan`
- `agent-fix-proposal`

What the agent can do:

- summarize scans and audits
- compare against benchmark context
- generate executive summaries
- produce normalized task bundles
- prepare fix proposals and issue-export payloads
- trigger alerts through webhook, email, or Telegram delivery paths

What the agent cannot do silently:

- publish production changes
- merge code or CMS changes without approval
- bypass the explicit approval boundary for risky actions
