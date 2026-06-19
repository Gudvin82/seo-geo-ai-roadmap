# AGENTS.md

## What this repository is

This project is a Discoverability OS for:

- SEO
- GEO and AI visibility
- factual consistency
- bilingual operator delivery
- self-hosted scanner and audit foundations

## Current core path for agents

Read in this order:

1. [README.md](./README.md)
2. [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
3. [METHODOLOGY.md](./METHODOLOGY.md)
4. [SCORING_EXPLAINED.md](./SCORING_EXPLAINED.md)
5. [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)
6. [PUBLIC_PRODUCT_READINESS.md](./PUBLIC_PRODUCT_READINESS.md)
7. [REAL_CASES.md](./REAL_CASES.md)

For Russian-language delivery also read:

- [README_RU.md](./README_RU.md)
- [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
- [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
- [AI_TASK_PACKS_RU.md](./AI_TASK_PACKS_RU.md)

## Hard boundary

Do not overclaim the repo.

Safe claims:

- self-hosted platform
- methodology plus app layer
- AI-agent-ready repo
- foundation for a scanner or audit service

Unsafe claims:

- finished hosted SaaS with maintainer-operated uptime
- fully autonomous production fixer
- guaranteed rankings or guaranteed AI citations

## How to use docs correctly

The repo has:

- deep playbooks
- compact checklists
- prompts and task packs
- scripts
- app surfaces
- historical archive documents

Rule:

- do not treat `checklists/` as the whole methodology
- do not treat historical `*-vXYZ.md` files as the primary explanation
- use current root docs first, archive docs second

## Default execution order

When a task sounds broad, use this order:

1. root entrypoints
2. relevant deep playbook
3. relevant checklist
4. relevant script or app flow
5. evidence or case reference
6. tests and validation

## AI deployment path

If the user asks to deploy:

1. clone the repo
2. create `.env`
3. run `make up`
4. run `make migrate`
5. run `make seed` if needed
6. verify frontend, API docs, and demo login

Fastest demo option:

- `make turnkey-demo`

## AI audit path

If the user asks to audit a site:

1. read [AI_TASK_PACKS.md](./AI_TASK_PACKS.md)
2. read the relevant playbook(s)
3. run repo-native scripts where possible
4. separate:
   - verified findings
   - heuristic findings
   - assumptions
5. produce a report plus prioritized backlog

## Mandatory self-check

Before claiming the work is ready:

1. run `make agent-self-check`
2. run `make verify-demo` if the stack is running
3. run the relevant tests if code changed

Then explicitly report:

- what was verified
- what was not verified
- what remains heuristic
- whether EN and RU layers are aligned
- whether public-positioning docs still match reality
