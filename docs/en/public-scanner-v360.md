# Public Scanner Foundation

`v3.6.0` adds a self-hosted/public-ready scanner foundation on top of the
existing app and audit flow.

## What this foundation includes

- dedicated intake page for passive, active, and full scan modes
- safe URL normalization and SSRF-oriented target blocking
- ownership verification for active or full scan modes
- consent recording for passive and active scan paths
- async scan jobs with status, events, and artifacts
- optional webhook, SMTP/email, and Telegram completion hooks

## Deployment modes

- Local dev:
  use for implementation and UI testing only
- Self-hosted internal:
  use for operator-only or agency-internal deployments
- Self-hosted public intake:
  expose the intake page only when reverse proxy, rate limiting, logging, and
  safe feature flags are configured

## Feature flags

Dangerous behavior stays off by default:

- `ALLOW_PUBLIC_INTAKE=false`
- `ALLOW_ACTIVE_SCAN=false`
- `ALLOW_ANONYMOUS_SUBMISSION=false`
- `ALLOW_FULL_SCAN=false`

Additional scanner controls:

- `SCANNER_ALLOWED_SCHEMES`
- `SCANNER_MAX_URL_LENGTH`
- `SCANNER_MAX_CONCURRENT_SUBMISSIONS_PER_IP`
- `SCANNER_VERIFICATION_TTL_MINUTES`
- `SCANNER_WEBHOOK_TIMEOUT_SECONDS`

## Threat model summary

This release is not a hardened multi-tenant public SaaS. It is a safe
self-hosted foundation.

Main threats considered in `v3.6.0`:

- SSRF against local, private, or metadata targets
- unauthorized active scanning of third-party domains
- unbounded public intake without feature flags
- long-running jobs with no visible lifecycle
- report delivery with no schema or event trail

## Abuse boundaries

- localhost, RFC1918, loopback, link-local, reserved, and metadata-style
  targets are blocked
- active and full scans require ownership verification and explicit consent
- submissions are throttled per IP and per domain
- dangerous modes remain feature-flagged

## Reverse proxy and rate-limit guidance

Recommended for public intake:

- terminate TLS at the reverse proxy
- add request rate limiting per IP
- cap request body size
- forward `X-Forwarded-For` correctly
- keep app access logs and reverse-proxy logs aligned

## Storage and retention

- verification records, consent records, scan jobs, and scan events are stored
  in the application database
- generated artifacts are stored under the configured artifact root
- define a cleanup policy before enabling high-volume public intake

## Privacy notice template

Suggested operator notice:

> This self-hosted scanner stores submitted URLs, verification records, consent
> confirmations, job events, and generated artifacts for operational and audit
> purposes.

## Responsible use statement

- do not use this scanner as a penetration-testing substitute
- do not run active scans without ownership or explicit authorization
- treat heuristic outputs as operator inputs, not legal or security guarantees
