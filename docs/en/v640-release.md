# v6.4.0 Release Summary

`v6.4.0` upgrades the repo from a strong foundation into a more operator-ready
delivery surface for managed runtime, tenant operations, portfolio review, and
proof follow-through.

## What changed

- added runtime-policy editing for integrations so managed-runtime expectations
  are machine-readable and operator-controlled
- added organization switcher, tenant usage health, quota alerts, onboarding
  checklist, and richer tenant overview fields
- expanded portfolio dashboards so operators can review a workspace, an entire
  organization, or all accessible workspaces in one rollup
- added `proof-ops-center` and richer proof rendering for evidence,
  experiments, confidence distribution, and next recommended steps
- upgraded the frontend so the new SaaS and proof surfaces are visible as
  cards and operator summaries instead of raw JSON only
- aligned active runtime, contract, and docs markers around `v6.4.0`

## Why it matters

Before `v6.4.0`, the repo already had a strong app and API foundation, but
managed-runtime execution still felt more backend-first than operator-first.

After `v6.4.0`, teams can more easily:

- understand which integrations are truly managed-runtime ready
- review tenant usage and onboarding pressure before it becomes a support issue
- operate across multiple workspaces or organizations from one portfolio layer
- track evidence and experiments as an execution loop rather than static proof

## Honest boundary

`v6.4.0` still does **not** mean:

- a maintainer-run hosted SaaS
- full billing, SSO, or zero-touch enterprise onboarding
- that every live integration is already fully plug-and-play in every
  environment

It does mean the repo is more operationally complete for self-hosted teams that
want a real delivery surface instead of docs-only foundations.
