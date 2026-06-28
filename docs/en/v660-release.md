# v6.6.0 Release Summary

`v6.6.0` closes one more maturity gap between a strong self-hosted foundation
and a cleaner operator-ready platform by adding tenant admin visibility,
managed-integration proof, and stricter release hygiene.

## What changed

- added `tenant-admin-console` so operators can review tenant profiles, plan
  posture, quota pressure, onboarding state, and API key counts in one place
- added `managed-integration-center` so first-class search, analytics, paid,
  local, RU, and Alice AI surfaces are visible as one managed runtime matrix
- added `docs-consolidation-center` to make the current doc path, AI-agent path,
  service-builder path, and archive policy explicit inside the product layer
- exposed the new admin, docs, and managed-integration centers directly in the
  frontend instead of leaving them backend-only
- added `release-hygiene` CI to verify version markers, release docs, docs
  build, and frontend syntax as part of release discipline

## Why it matters

Before `v6.6.0`, the repo already had stronger runtime ops, SEO maturity, and
evidence surfaces, but some service-builder and release-governance layers still
felt more implied than productized.

After `v6.6.0`, teams can more easily:

- operate multiple tenant profiles with clearer quota and onboarding visibility
- judge whether key integrations are still starter-first, live-runtime, or
  closer to managed-runtime discipline
- route new users through a cleaner current-docs path instead of relying on
  repo archaeology
- reduce version drift between backend, frontend, and public-facing docs

## Honest boundary

`v6.6.0` still does **not** mean:

- a maintainer-operated hosted SaaS
- billing and subscription product maturity
- zero-touch external integrations in every deployment

It does mean the free self-hosted platform is now more honest, more observable,
and more usable as a multi-tenant operator system.
