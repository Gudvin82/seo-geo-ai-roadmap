# AGENTS.md

## Project summary

This repository is a Discoverability OS for SEO, GEO, AI visibility, and
multilingual discoverability across global and Russian-speaking markets.

Start here if you are an AI coding agent working inside the repository:

- [README.md](./README.md)
- [README_RU.md](./README_RU.md)
- [WALKTHROUGH.md](./WALKTHROUGH.md)
- [REAL_CASES.md](./REAL_CASES.md)

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
3. glossary
4. relevant docs
5. matching checklist
6. matching prompts
7. matching scripts
8. matching examples
9. tests and validation
10. PR template and Definition of Done

## Commands and scripts

### Core scripts

```bash
python scripts/check-robots-ai-bots.py --url https://example.com
python scripts/generate_llms_txt.py --sitemap-url https://example.com/sitemap.xml
python scripts/ai-share-of-voice-tracker.py "Example AI Agency" --queries "best GEO agency,ai visibility audit"
python scripts/sitemap-checker.py --url https://example.com/sitemap.xml
python scripts/roi_calculator.py --traffic 5000 --conversion-rate 0.03 --lead-to-sale-rate 0.2 --average-check 1200 --margin-rate 0.45 --seo-cost 1500
python scripts/content_freshness_checker.py --sitemap-file ./sitemap.xml --days-stale 180 --output-file ./freshness.md
python scripts/check_hallucinations.py --brand-facts-file examples/brand-facts-example.md --questions-file examples/hallucination-questions-example.md --output-file ./hallucination-report.md
python -m pytest
```

### Before pushing changes

Prefer to:

```bash
python -m py_compile scripts/*.py
python -m pytest
```

and make sure repository workflows and markdown checks still make sense.

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
