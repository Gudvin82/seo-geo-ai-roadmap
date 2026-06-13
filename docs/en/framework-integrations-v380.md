# Framework Integrations v3.8.0

The repository remains framework-agnostic, but `v3.8.0` packages clearer
integration patterns for:

- Next.js or static React frontends
- Astro content sites
- WordPress or headless CMS sites
- self-hosted scanner intake pages

## Recommended pattern

1. keep the repo as the audit and reporting core
2. expose scanner intake behind your own domain or client area
3. connect provider configs and notifications per workspace
4. export graph JSON, fix packs, and reports into your delivery workflow

## Why this matters

The repository is easier to integrate when the command layer, graph layer, and
deliverables are explicit instead of implicit.
