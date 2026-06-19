# GEO and AI Operations Playbook

This playbook exists to move GEO from “interesting concept” to “repeatable operating loop”.

## The loop

1. define tracked entities, offers, and claims
2. define tracked prompts and answer surfaces
3. review AI answers manually or through bounded tooling
4. capture factual drift, citation behavior, and omission patterns
5. patch trust pages, facts, FAQ, and answer-ready content
6. re-run and compare

## What to monitor

- brand mention yes or no
- citation presence
- source URL quality
- factual accuracy
- claim drift
- competitor presence
- trust-page usage
- RU-specific behavior such as YandexAdditional and Yandex Neuro surfaces

## What usually breaks

- the brand is mentioned but not cited
- the brand is cited but framed ambiguously
- outdated facts are reused
- case-study and proof pages are weak
- FAQ and definition layers are too thin
- AI-facing files exist but do not match the real site

## What to fix first

1. factual contradictions
2. missing canonical trust pages
3. weak answer-ready blocks
4. poor entity linking between homepage, about, services, cases, and legal pages
5. AI file misalignment across `robots.txt`, `llms.txt`, `ai.txt`, and sitemap

## Evidence discipline

Every GEO cycle should preserve:

- prompt used
- provider or surface checked
- date
- observed answer
- citation state
- mismatch notes
- what was changed afterward

Without this, GEO becomes storytelling instead of operations.

## Outputs

- AI visibility audit log
- factual drift log
- entity and trust backlog
- answer-ready content backlog
- before / after evidence pack
