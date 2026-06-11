# SEO + GEO + AI Discoverability OS

[![Version](https://img.shields.io/github/v/tag/Gudvin82/seo-geo-ai-roadmap?label=version)](https://github.com/Gudvin82/seo-geo-ai-roadmap/tags)
[![License](https://img.shields.io/github/license/Gudvin82/seo-geo-ai-roadmap)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Gudvin82/seo-geo-ai-roadmap)](https://github.com/Gudvin82/seo-geo-ai-roadmap/commits/main)
[![Markdown Lint](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Gudvin82/seo-geo-ai-roadmap/actions/workflows/markdown-lint.yml)

Not another SEO checklist. An operating system for search, AI visibility, and multilingual discoverability.

[Русская версия](./README_RU.md)

## Why this repository exists

This project is built as an execution-first framework for teams that need one practical system across classic SEO, GEO, AI discoverability, Yandex, content operations, governance, reporting, and release discipline.

## Differentiators

- Bilingual by design: English and Russian are both first-class layers, not a translated afterthought.
- Google + Yandex + LLM in one framework: global search, Russian-speaking markets, and AI surfaces are handled together.
- Execution-first structure: docs, checklists, prompts, templates, scripts, and examples reinforce each other.
- AI-native layer: `llms.txt`, AI bots, answer-ready content, hallucination fixes, and AI share-of-voice monitoring are built in.
- Governance-ready: RACI, Definition of Done, implementation roadmap, release process, and reporting templates are included.
- Discoverability framing: the repository treats visibility as a system wider than SEO alone.

## Who it is for

- In-house SEO, growth, and content teams
- Agencies serving both RU/CIS and global markets
- Founders and operators building multilingual lead generation websites
- Teams that need practical SOPs instead of theoretical SEO checklists

## What is inside

- Deep bilingual docs in [`docs/en`](./docs/en) and [`docs/ru`](./docs/ru)
- Operational checklists in [`checklists`](./checklists)
- Prompt library in [`prompts`](./prompts)
- Reusable templates in [`templates`](./templates)
- Validation and helper scripts in [`scripts`](./scripts)
- Filled samples in [`examples`](./examples)
- Positioning, governance, ecosystem, and release documentation in the repository root

## Quick start

1. Read [POSITIONING.md](./POSITIONING.md) and [DIFFERENTIATORS.md](./DIFFERENTIATORS.md).
2. Start from [docs/en/01-audit.md](./docs/en/01-audit.md).
3. Build the page plan with [docs/en/04-page-matrix.md](./docs/en/04-page-matrix.md).
4. Implement AI visibility with [docs/en/08-geo-ai-search.md](./docs/en/08-geo-ai-search.md).
5. Set reporting discipline with [docs/en/18-analytics.md](./docs/en/18-analytics.md) and [ROADMAP.md](./ROADMAP.md).

## Example script

The repository includes real helper scripts, not just documentation. One useful
entry point is [`scripts/generate_llms_txt.py`](./scripts/generate_llms_txt.py),
which builds `llms.txt` from a sitemap.

### Generate llms.txt from sitemap

```bash
python scripts/generate_llms_txt.py \
  --sitemap-url https://example.com/sitemap.xml \
  --output-file ./llms.txt
```

Sample output:

```text
Processed URLs: 42
Output file: llms.txt
Warnings:
- Review description for https://example.com/solutions/ai-ops
```

## Example prompt

Use the `llms.txt` generator prompt when you want an AI assistant to draft a
human-readable `llms.txt` structure before review.

Purpose: turn a sitemap and key pages into a concise `llms.txt` draft.

Input: homepage, service pages, FAQ, about page, and a sitemap.

```text
Role: technical discoverability specialist
Inputs: https://example.com, homepage, service pages, FAQ, about page
Task: produce a production-ready llms.txt draft with concise descriptions
Output format: one line per URL with a short description
Evaluation criteria: conciseness, coverage, canonical discipline
```

## How to use this framework on a real project

1. Run the initial audit with [docs/en/01-audit.md](./docs/en/01-audit.md),
   [checklists/en/technical-seo-checklist.md](./checklists/en/technical-seo-checklist.md),
   and [`scripts/sitemap-checker.py`](./scripts/sitemap-checker.py).
2. Fix technical SEO using
   [docs/en/05-technical-seo.md](./docs/en/05-technical-seo.md) and
   [`scripts/check-robots-ai-bots.py`](./scripts/check-robots-ai-bots.py).
3. Implement GEO / AI visibility with
   [docs/en/08-geo-ai-search.md](./docs/en/08-geo-ai-search.md),
   [`scripts/generate_llms_txt.py`](./scripts/generate_llms_txt.py), and
   [`prompts/en/llms-txt-generator-prompt.md`](./prompts/en/llms-txt-generator-prompt.md).
4. Adapt the system for local or international markets through
   [docs/en/13-russia-yandex.md](./docs/en/13-russia-yandex.md) or
   [docs/en/12-international-seo.md](./docs/en/12-international-seo.md).
5. Improve content and answer extraction with
   [docs/en/07-content-eeat.md](./docs/en/07-content-eeat.md) and
   [prompts/en/answer-ready-page-prompt.md](./prompts/en/answer-ready-page-prompt.md).
6. Track analytics and AI visibility with
   [docs/en/18-analytics.md](./docs/en/18-analytics.md),
   [`scripts/ai-share-of-voice-tracker.py`](./scripts/ai-share-of-voice-tracker.py),
   and [examples/ai-share-of-voice-weekly-report.md](./examples/ai-share-of-voice-weekly-report.md).
7. Govern releases with [docs/en/20-raci.md](./docs/en/20-raci.md),
   [docs/en/21-definition-of-done.md](./docs/en/21-definition-of-done.md), and
   [RELEASE_PROCESS.md](./RELEASE_PROCESS.md).

## Architecture

```text
repo/
├── README.md / README_RU.md
├── POSITIONING.md / DIFFERENTIATORS.md / ECOSYSTEM_MAP.md
├── ROADMAP.md / RELEASE_PROCESS.md / CHANGELOG.md
├── docs/en and docs/ru
├── checklists/en and checklists/ru
├── prompts/en and prompts/ru
├── templates/ and templates/schema
├── scripts/
├── examples/
└── .github/
```

## Ecosystem references

This repository complements, not replaces, adjacent products and platforms. See [ECOSYSTEM_MAP.md](./ECOSYSTEM_MAP.md) for OpenSEO, Perplexica, Open WebUI, Trieve, Onyx, and Flowise.

## Roadmap preview

- Foundation: audit, architecture, page matrix, technical SEO, GEO/AI layer
- Execution: content quality, Yandex/RU specifics, analytics, governance, DoD
- Expansion: AI brand monitoring, international rollout, ongoing release discipline

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md), [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md), and the pull request template in [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md).
