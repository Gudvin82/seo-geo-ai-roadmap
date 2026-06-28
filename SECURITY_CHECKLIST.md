# Security Checklist

## Authentication and passwords

- Passwords are hashed with Argon2id, not plain SHA-256.
- Use a strong `APP_SECRET_KEY` in every non-local environment.
- Keep the minimum password policy in place:
  - at least 12 characters
  - uppercase
  - lowercase
  - numeric characters
- Do not reuse demo credentials in real deployments.

## Token lifecycle

- Access tokens must expire.
- Review `APP_TOKEN_TTL_MINUTES` before production rollout.
- Revoke tokens on user sign-out.
- Avoid indefinite-lived bearer tokens.

## Brute-force protection

- Keep the login attempt window enabled.
- Review `APP_LOGIN_ATTEMPT_LIMIT`.
- Review `APP_LOGIN_ATTEMPT_WINDOW_SECONDS`.
- Put the app behind a reverse proxy or edge rate limiter in production.

## Secrets and provider keys

- Never commit real provider API keys.
- Store provider keys in environment variables or secret managers.
- Rotate credentials after incident response or team changes.
- Limit who can view deployment secrets.

## Database and infrastructure hygiene

- Replace all sample database passwords.
- Use dedicated database users.
- Enable backups for PostgreSQL volumes or managed instances.
- Restrict direct database access to trusted operators only.

## HTTPS and reverse proxy expectations

- Terminate HTTPS at Nginx, Caddy, Traefik, or a managed load balancer.
- Do not expose the app publicly over plain HTTP in production.
- Keep forwarded headers and origin settings aligned with deployment reality.

## Workspace isolation and artifacts

- Confirm each user only sees their own workspaces and projects.
- Review artifact storage permissions.
- Back up exported reports and artifacts if they matter operationally.

## Dependency and platform maintenance

- Update Python dependencies on a regular schedule.
- Re-run tests after dependency upgrades.
- Watch for framework security advisories.
- Review provider API changes before production upgrades.

## CI security checks in `v3.3.0`

- `pip-audit` runs in GitHub Actions against `app/backend/requirements.txt`.
- `gitleaks` runs in GitHub Actions to catch likely committed secrets.
- Python CI now generates a coverage artifact so reviewers can inspect critical-path test reach.
- `v6.3.0` keeps dependency scanning strict, but documents the remaining
  baseline ignores in
  [SECURITY_ADVISORY_BASELINE.md](./SECURITY_ADVISORY_BASELINE.md) instead of
  silently swallowing dependency scan failures.

## What these checks do not guarantee

- They do not replace manual review of auth, permissions, or business-logic risk.
- They do not guarantee third-party endpoint safety.
- They do not turn the repository into a managed security service.
