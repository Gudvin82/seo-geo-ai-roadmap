# v5.0.0 Release Summary

`v5.0.0` is the SaaS productization, AI-to-App delivery, and executive
operating system release.

## What changed

- Added a stronger SaaS box foundation with organization, tenant profile, API
  key, onboarding, role, and usage abstractions.
- Added provider-detail runtime views with sync history, freshness, readiness,
  provenance, retry state, and recommended next actions.
- Added proof and attribution primitives for labeled evidence records,
  experiment history, before/after snapshots, and confidence labels.
- Added AI-to-App generation contracts, generated project manifests, and
  one-link build guidance so an AI agent can scaffold a working project shell
  under a machine-readable contract.
- Added onboarding-center and operator-center API surfaces to make deployment,
  setup, troubleshooting, and recurring operations more productized.

## Main product pillars

- Live integration maturity
- Executive intelligence
- Attribution and evidence
- SaaS box foundation
- AI-to-App delivery mode
- Operator and productization layer
- Bilingual EN and RU product quality

## New API surfaces

- `GET /api/v1/integrations/{integration_id}/detail`
- `GET /api/v1/saas/organizations`
- `POST /api/v1/saas/organizations`
- `GET /api/v1/saas/tenant-profiles`
- `POST /api/v1/saas/tenant-profiles`
- `GET /api/v1/saas/tenant-overview`
- `GET /api/v1/saas/api-keys`
- `POST /api/v1/saas/api-keys`
- `GET /api/v1/proof/labels`
- `GET /api/v1/proof/evidence`
- `POST /api/v1/proof/evidence`
- `GET /api/v1/proof/experiments`
- `POST /api/v1/proof/experiments`
- `GET /api/v1/generation/contracts`
- `POST /api/v1/generation/manifests/generate`
- `GET /api/v1/generation/manifests`
- `GET /api/v1/settings/onboarding-center`
- `GET /api/v1/settings/operator-center`

## New operator entrypoints

- [Build With This Platform](../../BUILD_WITH_THIS_PLATFORM.md)
- [Generate Project From URL](../../GENERATE_PROJECT_FROM_URL.md)

## Honest boundary

`v5.0.0` makes the repository look and behave more like a real SaaS foundation,
but it does not claim a maintainer-operated hosted SaaS, turnkey enterprise
billing, or complete enterprise SSO out of the box.
