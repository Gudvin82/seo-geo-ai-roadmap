# Start Here For AI

Use this file when a user wants an AI coding agent to deploy, audit, adapt, or
evaluate this repository honestly.

## First: understand what this repo is

This repository is:

- open-source
- self-hosted
- AI-agent-ready
- methodology plus app plus scripts

This repository is not:

- a finished hosted SaaS operated by the maintainer
- a silent autopilot for production changes
- a replacement for human approval on risky work

Read first:

1. [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
2. [METHODOLOGY.md](./METHODOLOGY.md)
3. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
4. [REAL_CASES.md](./REAL_CASES.md)

## Fastest safe deployment path

If the user says “deploy this for me”:

1. `git clone https://github.com/Gudvin82/seo-geo-ai-roadmap.git`
2. `cd seo-geo-ai-roadmap`
3. `cp .env.example .env`
4. fill required keys or keep demo-safe defaults
5. `make up`
6. `make migrate`
7. `make seed` if demo data is needed
8. verify:
   - `http://localhost:3000`
   - `http://localhost:8000/docs`
   - demo login works

Fastest demo route:

- `make turnkey-demo`

## If the user wants a ready-made prompt

Start here:

- [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)

Also available:

- [prompts/en/repo-site-audit-agent-prompt.md](./prompts/en/repo-site-audit-agent-prompt.md)
- [prompts/en/deploy-client-scanner-agent-prompt.md](./prompts/en/deploy-client-scanner-agent-prompt.md)
- [prompts/en/improve-existing-site-agent-prompt.md](./prompts/en/improve-existing-site-agent-prompt.md)

## Core AI working order

When in doubt, use this order:

1. [README.md](./README.md)
2. [AGENTS.md](./AGENTS.md)
3. [METHODOLOGY.md](./METHODOLOGY.md)
4. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
5. [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)
6. the relevant deep playbook in `docs/en/`
7. the relevant checklist in `checklists/`
8. the relevant script in `scripts/`
9. [REAL_CASES.md](./REAL_CASES.md)

## If the task is “audit a site”

Use:

- [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)
- [docs/en/technical-seo-deep-playbook.md](./docs/en/technical-seo-deep-playbook.md)
- [docs/en/semantic-core-and-intent-playbook.md](./docs/en/semantic-core-and-intent-playbook.md)
- [docs/en/geo-ai-operations-playbook.md](./docs/en/geo-ai-operations-playbook.md)

Then prefer repo-native helpers such as:

- `python scripts/check-robots-ai-bots.py --url https://example.com`
- `python scripts/check-ai-txt.py --url https://example.com`
- `python scripts/check-llms-txt.py --url https://example.com/llms.txt`
- `python scripts/schema-coverage-checker.py --url https://example.com --site-type service`
- `python scripts/faq-detector.py --url https://example.com`
- `python scripts/open-graph-checker.py --url https://example.com`
- `python scripts/rag_chunk_audit.py --url https://example.com`
- `python scripts/citability_score.py --url https://example.com`

## Mandatory self-check before saying “done”

If code or runtime behavior changed:

1. run `make agent-self-check`
2. run `make verify-demo` if the stack is running
3. run the relevant test path

Always report:

- what was actually verified
- what was heuristic
- what still needs human review
- whether EN and RU user-facing layers were both updated
