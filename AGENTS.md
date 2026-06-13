# AGENTS.md

## Project summary

This repository is a Discoverability OS for SEO, GEO, AI visibility, and
multilingual discoverability across global and Russian-speaking markets.

Start here if you are an AI coding agent working inside the repository:

- [README.md](./README.md)
- [README_RU.md](./README_RU.md)
- [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
- [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- [ARCHITECTURE_NOTE.md](./ARCHITECTURE_NOTE.md)
- [ARCHITECTURE_NOTE_RU.md](./ARCHITECTURE_NOTE_RU.md)
- [WALKTHROUGH.md](./WALKTHROUGH.md)
- [REAL_CASES.md](./REAL_CASES.md)

## For AI Agents: Deploy this project from scratch

If a user asks you to "deploy this SEO platform", follow this order:

1. Run `git clone https://github.com/Gudvin82/seo-geo-ai-roadmap.git`
2. Run `cd seo-geo-ai-roadmap`
3. Run `cp .env.example .env` and help the user fill required keys or keep demo-safe defaults for local testing
4. Run `make up`
5. Run `make migrate`
6. Run `make seed` if demo data is needed
7. Output:
   - `http://localhost:3000`
   - `http://localhost:8000/docs`
   - demo credentials `demo@example.com` / `DemoPlatform123`

Fastest all-in-one option for a lazy demo deployment:

- run `make turnkey-demo`

Canonical operator path in `v3.8.0`:

- `/geo quick`
- `/geo audit`
- `/geo graph`
- `/geo report`
- `/geo compare`

If the user wants a ready task prompt instead of inventing one:

- run `python scripts/agent_handoff_pack.py --task deploy-demo --language en`
- run `python scripts/agent_handoff_pack.py --task audit-site --language ru --target-url https://example.com`
- run `python scripts/agent_handoff_pack.py --task deploy-scanner --language en`

If the user wants a public or semi-public scanner intake flow:

- open `app/frontend/scanner.html`
- open `app/frontend/graph.html` for issue and trust explainability
- read `docs/en/public-scanner-v360.md` or `docs/ru/public-scanner-v360.md`
- read `docs/en/discoverability-coverage-v370.md` or `docs/ru/discoverability-coverage-v370.md`
- use `GET /api/v1/scanner/config` before exposing scan modes in UI
- require ownership verification before `active` or `full` scans
- use `POST /api/v1/scan-jobs` and poll `GET /api/v1/scan-jobs/{id}`

## For AI Agents: Mandatory self-check before claiming "done"

Before saying the project is ready, deployed, or turnkey, run:

1. `make agent-self-check`
2. `make verify-demo` if the stack is running
3. `python -m pytest` or the repo-equivalent validation path if code changed

The agent must then self-report:

- what was actually verified
- what was not verified
- whether the result is safe for demo only or production-like self-hosting
- whether EN and RU layers were both updated when user-facing scope changed
- whether `START_HERE_FOR_AI*.md`, handoff prompts, and client playbooks still match reality

## Roles and typical tasks for agents

### 1. Set up `llms.txt` for a domain

Use:

- [scripts/generate_llms_txt.py](./scripts/generate_llms_txt.py)
- [templates/llms.txt.example](./templates/llms.txt.example)
- [docs/en/08-geo-ai-search.md](./docs/en/08-geo-ai-search.md)

Typical flow:

1. Load sitemap via `--sitemap-url` or `--sitemap-file`.
2. Generate a first `llms.txt` draft.
3. Review public URLs and descriptions.
4. Update examples or docs if the process changes.

### 2. Run a full GEO / AI audit

Use:

- [docs/en/01-audit.md](./docs/en/01-audit.md)
- [docs/en/08-geo-ai-search.md](./docs/en/08-geo-ai-search.md)
- [checklists/en/geo-ai-visibility-checklist.md](./checklists/en/geo-ai-visibility-checklist.md)
- [scripts/check-robots-ai-bots.py](./scripts/check-robots-ai-bots.py)
- [scripts/ai-share-of-voice-tracker.py](./scripts/ai-share-of-voice-tracker.py)

### 3. Prepare a page matrix and Definition of Done for a new site section

Use:

- [docs/en/04-page-matrix.md](./docs/en/04-page-matrix.md)
- [docs/en/21-definition-of-done.md](./docs/en/21-definition-of-done.md)
- [checklists/en/page-definition-of-done-checklist.md](./checklists/en/page-definition-of-done-checklist.md)
- [templates/page-brief-template.md](./templates/page-brief-template.md)

## Repository map for agents

### What the main folders mean

- `docs/`: operating manual and execution logic
- `checklists/`: task-ready execution lists
- `prompts/`: reusable AI prompts
- `templates/`: reusable assets and starter files
- `scripts/`: validation and automation helpers
- `app/`: SaaS-ready backend, frontend, and shared product layer
- `docker-compose.yml`: self-hosted product stack
- `infra/` and `docker/`: deployment notes and container assets
- `alembic/`: database migration layer
- `examples/`: realistic filled examples
- `tests/`: pytest validation for key scripts
- `automation/`: starter automation assets

### What to read first

1. [POSITIONING.md](./POSITIONING.md)
2. [DIFFERENTIATORS.md](./DIFFERENTIATORS.md)
3. [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)
4. [docs/en/01-audit.md](./docs/en/01-audit.md) for audits
5. [docs/en/08-geo-ai-search.md](./docs/en/08-geo-ai-search.md) for GEO / AI work
6. [docs/en/canonical-facts-and-entity-consistency.md](./docs/en/canonical-facts-and-entity-consistency.md)
7. [docs/en/entity-hierarchy-and-brand-focus.md](./docs/en/entity-hierarchy-and-brand-focus.md)

## Execution rules

Agents should:

- avoid changing the folder structure unless explicitly asked
- reuse existing templates, checklists, prompts, and scripts
- update relevant examples or docs when behavior changes
- respect [docs/en/21-definition-of-done.md](./docs/en/21-definition-of-done.md)
  and [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md)
- prefer repository defaults before inventing a new workflow

If the user gives a broad command such as:

- "make it production-ready"
- "set everything up end-to-end"
- "prepare this repo for a real project"

then default to the project workflow already described in:

- [README.md](./README.md)
- [docs/en/21-definition-of-done.md](./docs/en/21-definition-of-done.md)
- [RELEASE_PROCESS.md](./RELEASE_PROCESS.md)

## Default execution path for turnkey tasks

When a task sounds like "set everything up", "do it turnkey", "adapt this under
the repo", or "take the best option", use this default order:

1. `README.md` or `README_RU.md` for framing
2. `AGENTS.md` for execution rules
3. the relevant file in `docs/`
4. matching `checklists/`
5. matching `prompts/`
6. matching `scripts/`
7. matching `examples/`
8. Definition of Done and the PR template
9. tests and validation output

## Default workflow for implementation or audit tasks

Use this order by default:

1. README
2. AGENTS
3. START_HERE_FOR_AI
4. glossary
5. relevant docs
6. matching checklist
7. matching prompts
8. matching scripts
9. matching examples
10. tests and validation
11. PR template and Definition of Done

## Commands and scripts

### Core scripts

```bash
python scripts/geo_command_surface.py catalog --format markdown
python scripts/agent_handoff_pack.py --task audit-site --language en --target-url https://example.com
python scripts/bootstrap_self_hosted.py --mode demo --format markdown
python scripts/bootstrap_self_hosted.py --mode scanner --format markdown
python scripts/check-robots-ai-bots.py --url https://example.com
python scripts/check-ai-txt.py --url https://example.com
python scripts/schema-coverage-checker.py --url https://example.com --site-type service
python scripts/faq-detector.py --url https://example.com
python scripts/open-graph-checker.py --url https://example.com
python scripts/robots-sitemap-link-checker.py --url https://example.com
python scripts/generate_llms_txt.py --sitemap-url https://example.com/sitemap.xml
python scripts/ai-share-of-voice-tracker.py "Example AI Agency" --queries "best GEO agency,ai visibility audit"
python scripts/sitemap-checker.py --url https://example.com/sitemap.xml
python scripts/roi_calculator.py --traffic 5000 --conversion-rate 0.03 --lead-to-sale-rate 0.2 --average-check 1200 --margin-rate 0.45 --seo-cost 1500
python scripts/content_freshness_checker.py --sitemap-file ./sitemap.xml --days-stale 180 --output-file ./freshness.md
python scripts/check_hallucinations.py --brand-facts-file examples/brand-facts-example.md --questions-file examples/hallucination-questions-example.md --output-file ./hallucination-report.md
python -m pytest
python -m pytest app/backend/tests
```

### GEO command surface

If the user request sounds like one of these commands, route through the matching
surface first:

- `audit`
- `quick`
- `citability`
- `crawlers`
- `deploy`
- `llmstxt`
- `brands`
- `platforms`
- `scanner`
- `schema`
- `technical`
- `content`
- `report`
- `compare`

Use:

```bash
python scripts/geo_command_surface.py catalog
python scripts/geo_command_surface.py audit --format json
```

This gives the recommended docs, scripts, API routes, and next step for each
task type.

### App-layer entrypoints

- `app/backend/app/main.py`
- `app/backend/app/api/`
- `app/backend/app/services/`
- `app/backend/app/providers/`
- `app/frontend/index.html`
- `DEPLOYMENT.md`
- `ARCHITECTURE.md`
- `SECURITY_CHECKLIST.md`
- `docs/en/api-reference.md`
- `docs/en/ai-operator-mode.md`
- `docs/en/public-scanner-v360.md`
- `docs/ru/public-scanner-v360.md`
- `docs/en/discoverability-coverage-v370.md`
- `docs/ru/discoverability-coverage-v370.md`
- `app/frontend/scanner.html`
- `app/frontend/scanner.js`

If the user asks for a turnkey product foundation or self-hosted SaaS setup,
agents should preserve the methodology layer and extend the app layer instead of
replacing the repository with a standalone application.

### Before pushing changes

Prefer to:

```bash
python -m py_compile scripts/*.py
python -m pytest
```

and make sure repository workflows and markdown checks still make sense.

### Agent self-check

```bash
make agent-self-check
```

This script is a repository-level sanity check for AI agents. It verifies that
the core turnkey promises still exist: README framing, AGENTS entrypoint, app
layer, deployment docs, operator docs, proof assets, local LLM layer, and the
self-check mechanism itself.

### Handoff files for lazy or delegated AI execution

- [START_HERE_FOR_AI.md](./START_HERE_FOR_AI.md)
- [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
- [CLIENT_SETUP_PLAYBOOK.md](./CLIENT_SETUP_PLAYBOOK.md)
- [CLIENT_SETUP_PLAYBOOK_RU.md](./CLIENT_SETUP_PLAYBOOK_RU.md)
- [AI_HANDOFF_PROMPT.md](./AI_HANDOFF_PROMPT.md)
- [AI_HANDOFF_PROMPT_RU.md](./AI_HANDOFF_PROMPT_RU.md)

## Docs-site workflow

Local preview:

```bash
pip install mkdocs-material
mkdocs serve
```

Build only:

```bash
mkdocs build
```

If GitHub Pages fails:

- inspect `mkdocs.yml`
- confirm navigation paths exist
- check the Pages workflow on `main`
- enable repository Pages settings and set `ENABLE_GITHUB_PAGES=true` before
  expecting deploy to run
- rebuild locally before editing workflow YAML

## Definition of Done

Full references:

- [docs/en/21-definition-of-done.md](./docs/en/21-definition-of-done.md)
- [docs/ru/21-definition-of-done.md](./docs/ru/21-definition-of-done.md)

Short version:

- page intent is clear and covered
- title, meta, and heading structure are reviewed
- schema is valid where relevant
- analytics or measurement is configured where relevant
- internal links are added
- AI/GEO checks are completed where applicable

Any agent closing a task should review these items and keep the pull request
template aligned with the task outcome.

## When to ask the user

Ask for clarification when:

- priorities conflict and there is no ranking criterion
- sitemap access or source files are missing
- the request says "take the best option" without decision criteria
- the repository or production target introduces destructive risk
- a turnkey request could be implemented in more than one high-impact way

## Russian quick note

Если вы используете русскоязычный ИИ или IDE, логика та же.

Основные файлы:

- [README_RU.md](./README_RU.md)
- [docs/ru](./docs/ru)
- [checklists/ru](./checklists/ru)
- [prompts/ru](./prompts/ru)
- [scripts](./scripts)
- [REAL_CASES_RU.md](./REAL_CASES_RU.md)
- [WALKTHROUGH_RU.md](./WALKTHROUGH_RU.md)

DoD, release discipline и execution rules не меняются: агент должен работать
через существующие шаблоны, чеклисты и сценарии, а не изобретать новую
структуру без причины.
