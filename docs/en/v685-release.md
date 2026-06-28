# v6.8.5 Release Summary

`v6.8.5` adds the planned community, launch, and contributor-growth layer on
top of the stronger docs, proof, and operator tooling introduced in `v6.7.0`,
`v6.7.5`, and `v6.8.0`.

## What changed

- added `COMMUNITY.md`, `SHOWCASE.md`, and `LAUNCH_PACK.md` as root public
  entrypoints
- added bilingual community and launch docs inside `docs/en` and `docs/ru`
- added `scripts/community_showcase_builder.py` for compact proof or showcase
  indexing
- added `scripts/launch_pack_generator.py` for safe public-positioning packs
- added app-level community, participation, and launch centers so this layer is
  visible in the self-hosted product, not only in markdown

## Why it matters

Before `v6.8.5`, the repository already had strong methodology, proof, and
operator tooling. But the public adoption path still depended too much on
readers discovering the right files themselves.

After `v6.8.5`, teams can more easily:

- explain the project honestly in public
- route contributors into the right intake path
- show the strongest current proof surfaces faster
- reuse a launch narrative without overclaiming hosted-SaaS maturity
