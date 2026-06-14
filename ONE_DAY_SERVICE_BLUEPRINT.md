# One-Day Service Blueprint

This file answers a practical question:

- "How do I turn this repo into my own client-facing scanner or audit service in one day?"

The goal is not "build a unicorn SaaS in one day".
The goal is:

- deploy the repo
- brand it
- expose scanner intake safely
- run audits
- hand back reports and tasks

## Target result by the end of the day

You should have:

- one deployed self-hosted stack
- one branded frontend
- one public or semi-public scanner intake page
- one internal operator flow for review and delivery
- one repeatable way to export findings, recommendations, and tasks

## Recommended day plan

### Hour 1: deploy the stack

1. Clone the repo
1. Copy `.env.example` to `.env`
1. Run `make up`
1. Run `make migrate`
1. Run `make seed` if you want demo data
1. Run `make verify-demo`

## Hour 2: configure the operator side

1. Sign in to the app
1. Create one workspace
1. Create one project
1. Fill brand facts
1. Connect at least one provider or stay in starter mode for proof-first demo
1. Run one audit and one SoV check

## Hour 3: enable the public intake side

1. Open `app/frontend/scanner.html`
1. Decide whether your public mode is:
   - passive only
   - passive plus ownership-gated active
   - full, but still review-first
1. Keep ownership verification enabled for active scans
1. Keep public-service limitations visible in UI

## Hour 4: brand the service

1. Set workspace branding fields
1. Add your logo, report title, subtitle, and footer
1. Decide your public promise:
   - audit service
   - scanner intake
   - expert-led SEO plus GEO plus AI service

## Hour 5: prepare the delivery layer

1. Use report exports
1. Use patch pack generation
1. Use client delivery pack generation
1. Choose whether output goes to:
   - PDF or report artifact
   - internal task board
   - GitHub Issues
   - Notion, Trello, or Linear style handoff

## Hour 6: prepare AI handoff

Use the built-in AI entrypoints:

- [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
- [AGENTS.md](./AGENTS.md)
- `python scripts/agent_handoff_pack.py --task deploy-scanner --language en`

Also use the v4.4 prompt packs:

- [prompts/en/repo-site-audit-agent-prompt.md](./prompts/en/repo-site-audit-agent-prompt.md)
- [prompts/en/deploy-client-scanner-agent-prompt.md](./prompts/en/deploy-client-scanner-agent-prompt.md)
- [prompts/en/improve-existing-site-agent-prompt.md](./prompts/en/improve-existing-site-agent-prompt.md)

## Hour 7: create the public story

Your safe public positioning is:

- self-hosted
- open-source
- AI-agent-ready
- foundation for your own scanner or audit service

Do not promise:

- hosted SaaS by the repo maintainer
- enterprise billing and SSO out of the box
- silent autopilot site changes

## Hour 8: perform one real proof run

1. Run one real site audit
1. Export one report
1. Export one patch pack
1. Export one client delivery pack
1. Save screenshots of:
   - login
   - dashboard
   - scanner intake
   - report

## Minimum public architecture

For a practical first release, use:

- one VPS or VM
- Docker Compose
- PostgreSQL
- reverse proxy with HTTPS
- one frontend entrypoint
- one backend API
- one artifact storage path

## Safe version of the public promise

Safe:

- "Users can enter a URL and receive a structured SEO plus GEO plus AI audit flow that our team reviews and delivers."

More aggressive but still safe:

- "This repo can be deployed as the foundation for a client-facing scanner or audit service."

Not safe:

- "This is already a finished hosted SaaS with zero setup."

## Where to go next

- [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
- [ONE_CLICK_DEPLOY_OPTIONS.md](./ONE_CLICK_DEPLOY_OPTIONS.md)
- [DEPLOYMENT.md](./DEPLOYMENT.md)
- [REAL_CASES.md](./REAL_CASES.md)
