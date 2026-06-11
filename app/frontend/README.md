# Frontend App Shell

This directory contains the first UI layer for `v2.0.0`.

It is intentionally simple:

- static HTML, CSS, and JavaScript
- no build step required
- bilingual EN/RU labels
- connects directly to the FastAPI backend
- suitable for local demos, self-hosted pilot deployments, and future migration
  into a richer frontend stack if needed

## What it covers

- sign up and sign in
- workspace creation
- project onboarding
- brand facts / truth center input
- provider configuration
- audit run creation
- report and artifact browsing

## Local usage

Open [`index.html`](./index.html) directly for a quick interface preview, or run
the Docker setup from [`DEPLOYMENT.md`](../../DEPLOYMENT.md) to use the full
backend + frontend stack together.
