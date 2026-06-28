# Security Policy

## Scope

Use this path for security-sensitive problems in the repository, scripts, app
layer, scanner paths, or public deployment guidance.

Examples:

- auth or access-control bypass
- sensitive data exposure
- unsafe scanner behavior
- SSRF-like fetch issues
- unsafe secrets handling
- injection or privilege escalation risks

## Reporting

Please avoid opening a public issue first for a live security problem.

Report with:

- the affected path or file
- impact summary
- reproduction steps if safe
- whether the issue is local-only, self-hosted-only, or public-surface relevant

## Response Principles

The project aims to:

- confirm the issue
- understand scope and impact
- fix the problem honestly
- update docs and release notes when the issue affects public claims

## Current Security Position

The project includes security scans and runtime hardening, but it is still a
self-hosted platform with explicit boundaries.

Read:

- [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
- [WHAT_THIS_PROJECT_IS_NOT.md](./WHAT_THIS_PROJECT_IS_NOT.md)
