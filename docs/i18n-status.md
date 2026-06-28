# i18n Status

This file tracks bilingual parity for the most important repository surfaces.

## Current Status

| Surface | EN | RU | Notes |
| --- | --- | --- | --- |
| Root README | yes | yes | Both are active root entrypoints |
| Docs index | yes | yes | Current-docs-first routing |
| Methodology | yes | yes | Core methodological path |
| Public readiness | yes | yes | Public-safe wording path |
| AI agent entry | yes | yes | First-class AI handoff |
| Walkthrough | yes | yes | Human operator onboarding |
| Release summaries | yes | yes | Active releases should stay paired |
| Public cases | yes | yes | Keep fact and inference boundaries aligned |

## Parity Rules

- root entrypoints should exist in both English and Russian
- release-facing docs should exist in both English and Russian
- new current-docs surfaces should not land in one language only
- archive material can lag temporarily, but active docs should not

## Known Exceptions

- some historical materials may remain English-first or Russian-first
- some tool names and runtime labels stay in their original technical English

## Operator Rule

If a release changes public wording, onboarding, core methodology, or proof
positioning, update both languages in the same release.
