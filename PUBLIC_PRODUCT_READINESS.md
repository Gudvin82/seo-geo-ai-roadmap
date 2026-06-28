# Public Product Readiness

This file exists to make the repository's public promise precise.

Use it when someone asks:

- "Can I use this repo manually?"
- "Can I give this repo to Cursor, Claude Code, Codex, or VS Code?"
- "Can I deploy this as my own scanner or audit service?"
- "Is this already a hosted SaaS out of the box?"

## Short answer

Yes, the repository already supports three real use modes:

- manual framework use
- AI-agent-assisted audit and delivery use
- self-hosted product foundation for your own scanner or audit service

No, it should not be described as a finished public hosted SaaS with billing,
enterprise SSO, or maintainer-operated uptime guarantees.

Latest release context:

- `v6.8.0` adds stronger proof, case-library, synthetic training, and
  implementation-handoff tooling on top of the operator-tooling base introduced
  in `v6.7.5`

## What is production-ready today

- bilingual SEO, GEO, and AI methodology
- human-readable docs plus machine-readable contracts
- self-hosted FastAPI app with frontend, auth, workspaces, projects, reports,
  artifacts, and exports
- first-class SEO intelligence surface for keyword, competitor, backlink, and
  rank data
- scanner intake flow with passive, ownership-gated active, and full-scan modes
- governed CMS workflow with preview, approval, apply, verify, and rollback
- provider-backed AI layer for cloud and local runtimes
- CI workflows for markdown, scripts, docs, Python tests, links, and security scans
- public proof surfaces, including real case framing and demo screenshots

## What is strong but still foundation-level

- public scanner service for client-facing use
- webhook and notification operations
- queue and retry maturity for higher-volume production workloads
- managed cloud rollout packs
- GSC, GA4, Yandex, and CMS integrations as repeatable operator flows
- external keyword and authority providers as repeatable operator-owned flows
- extension and automation entrypoints

These paths are already inside the repo and can be deployed under your own
control, but they still expect operator review, infrastructure ownership, and
production decisions from the team using the repo.

## What is not part of the current promise

- maintainer-operated hosted SaaS
- enterprise SLA
- billing and subscription layer
- turnkey multi-tenant public abuse protection with zero operator setup
- guaranteed ranking or guaranteed AI citation outcomes
- silent fully autonomous site changes without human approval

## The three public-safe claims

### 1. Manual framework claim

Safe claim:

- "You can open the repo, read the methodology, and apply it manually."

Why this is safe:

- the repo contains docs, checklists, templates, prompts, scripts, and examples

### 2. AI-agent claim

Safe claim:

- "You can give this repo to an AI coding agent and ask it to audit the repo, audit a site by the repo methodology, and prepare a plan or report."

Why this is safe:

- the repo contains `AGENTS.md`, `START_HERE_FOR_AI*.md`,
  `contracts/*.schema.json`, task packs, and self-check paths

### 3. Product-foundation claim

Safe claim:

- "You can self-host this repo and use it as the foundation for your own scanner or audit service."

Why this is safe:

- the repo contains a real app layer, scanner intake, async jobs, exports,
  deployment guidance, cloud pack starters, and delivery flows

Boundary:

- this is a foundation and operating platform, not a finished hosted SaaS sold
  by the repo maintainer

## Best public wording

Recommended:

- "self-hosted platform"
- "open-source framework plus app layer"
- "foundation for your own audit or scanner service"
- "AI-agent-ready repo"

Avoid:

- "fully autonomous hosted SaaS out of the box"
- "enterprise scanner with no setup"
- "AI fixes any site automatically"

## Fast proof path

If you want to prove the repo matches the public post, use this path:

1. Read [README.md](./README.md)
1. Read [AGENTS.md](./AGENTS.md)
1. Read [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
1. Run `make turnkey-demo`
1. Run `make verify-demo`
1. Read [ONE_DAY_SERVICE_BLUEPRINT.md](./ONE_DAY_SERVICE_BLUEPRINT.md)
1. Read [ONE_CLICK_DEPLOY_OPTIONS.md](./ONE_CLICK_DEPLOY_OPTIONS.md)
1. Read [REAL_CASES.md](./REAL_CASES.md)

## Release alignment

`v6.7.0` is the release that makes this public promise easier to understand and
safer to hand off by adding:

- a stronger root README and quick-start structure
- a visual roadmap plus i18n-status visibility
- clearer support, security, and contribution guidance
- a cleaner current-docs-first routing path for humans and AI agents
