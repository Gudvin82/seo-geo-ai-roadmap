# Scheduled Operations

## Supported recurring checks

`v3.3.0` formalizes recurring execution for:

- AI Share of Voice checks
- audits
- `llms.txt`, robots, schema, and other structured checks

## Scheduling modes

- internal metadata only: useful for planning and app visibility
- cron-compatible CLI: run repository scripts from local cron, systemd timers, or a worker host
- GitHub Actions schedule: suitable for repo-driven public validation and lightweight checks

## Example schedules

- weekly `llms.txt` validation: Monday at 09:00
- weekly AI visibility snapshot: Tuesday at 10:00
- monthly full audit: first business day of the month

## Expected artifacts

- audit logs
- reports or patch packs
- CLI JSON output for automation
- notification events when configured

## Honest limitations

- local self-hosted users still need cron, Actions, or another scheduler
- `v3.3.0` is not a full queue scheduler with worker leasing
- recurring jobs should still be reviewed by humans before being treated as business truth
