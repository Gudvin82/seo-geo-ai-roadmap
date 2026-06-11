# Verify Deployment

This release was verified as a self-hosted operator flow, not just a static docs
drop.

## Fresh-path verification

1. Clone the repository and create `.env` from `.env.example`.
1. Install backend dependencies with `make install-backend`.
1. Apply schema changes with `make migrate`.
1. Seed demo data with `make seed`.
1. Start the stack with `make up` or use `./run-local.sh`.
1. Open:
   - `http://localhost:8000/healthz`
   - `http://localhost:8000/readyz`
   - `http://localhost:8000/docs`
   - `http://localhost:3000`
1. Log in with:
   - `demo@example.com`
   - `DemoPlatform123`
1. Open the seeded workspace and project.
1. Run `POST /api/v1/audit-runs/run` or launch an audit from the UI.
1. Confirm reports and artifacts are available.

## Expected outputs

- `healthz` returns `status: ok`
- `readyz` returns `status: ready`
- `/docs` loads successfully
- demo login returns a bearer token with expiry metadata
- workspace list is non-empty
- project list is non-empty
- audit run returns `audit_job_id` and `initial_status`
- reports endpoint returns at least one seeded or generated report
- artifacts endpoint returns at least one seeded or generated artifact

## Automated verification

Run:

```bash
make verify-demo
```

The command checks health, readiness, docs availability, demo auth, a minimal
audit run, and the presence of reports and artifacts.
