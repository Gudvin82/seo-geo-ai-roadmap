# Contributing

Thanks for helping improve the repository.

## Contribution Principles

- Prefer practical improvements over abstract commentary.
- Keep English and Russian structures aligned when the change affects both.
- Preserve the discoverability OS framing.
- Add examples, validation, templates, or proofs when expanding theory.
- Keep public claims honest and bounded.

## Good Contribution Types

- improve a playbook, checklist, or glossary entry
- add a reusable prompt, script, or validation helper
- submit a bounded public case with facts and explicit limits
- improve RU or EN parity
- fix broken links, stale version markers, or unclear onboarding paths

## Pull Request Flow

1. Open or reference an issue when the change is non-trivial.
2. Describe what changed and why it matters.
3. State whether EN and RU were both updated.
4. Include validation notes for scripts, tests, docs build, or link checks.
5. Keep the scope focused enough to review safely.

## Content Quality Bar

A contribution is stronger when it adds one or more of the following:

- an SOP that can be executed
- a checklist that can be used immediately
- a prompt that is copy-paste ready
- a template or example that reduces ambiguity
- a script that validates a repetitive task
- a case or proof artifact with fact/inference boundaries

## Naming And Formatting

- use lowercase file names with dashes when creating new content files
- keep one H1 per Markdown file
- keep RU and EN entrypoints structurally parallel where possible
- prefer concrete examples over generic advice

## Commit Style

Preferred commit prefixes:

- `feat:` new capability
- `fix:` bug or inconsistency fix
- `docs:` documentation improvement
- `test:` test coverage change
- `chore:` maintenance work

## Before You Submit

Run the relevant checks when possible:

```bash
python3 -m pytest tests -q
PYTHONPATH=app/backend python3 -m pytest app/backend/tests -q
python3 scripts/version_consistency_check.py
python3 scripts/release_hygiene_check.py
python3 -m mkdocs build
```

## Recognition

Meaningful contributors can be recognized in:

- future case or proof references
- contributor-facing roadmap notes
- release summaries when the work materially improves the project

## Questions

Use the current support path:

- [SUPPORT.md](./SUPPORT.md)
- [COMMUNITY.md](./COMMUNITY.md)
- open a GitHub issue for a concrete bug or broken path
- use discussions/community surfaces when they are enabled in the public repo
