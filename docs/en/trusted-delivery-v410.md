# Trusted Delivery Targets v4.1.0

`v4.1.0` adds a governed trusted-delivery layer for repositories where PRs may
be prepared for low-friction merge handling.

## What it adds

- `POST /api/v1/trusted-delivery-targets`
- `GET /api/v1/trusted-delivery-targets`
- `POST /api/v1/deliverables/pr-proposal`

## Why it matters

This moves the repo from generic "PR-ready payloads" to an explicit contract
for trusted repositories, required checks, and auto-merge eligibility.

## Important boundary

The system can now produce a PR proposal with:

- repository
- base branch
- branch name
- issue backlog
- required checks
- auto-merge eligibility flag

The actual merge still belongs to repository policy, credentials, and CI.
