# v6.3.0 Release Summary

`v6.3.0` is the release that tightens the gap between public methodology,
runtime behavior, and repo-level execution.

## What changed

- recalibrated current GEO and AI guidance so:
  - `llms.txt` is treated as an optional AI-routing surface
  - `reasoning.json` and `.well-known/ai-manifest.json` are treated as
    experimental extras
  - visible structure, schema, and answer-ready content matter more than
    speculative files
- added `OAI-SearchBot` coverage to the AI bot model
- upgraded `robots.txt` evaluation to handle multi-agent groups and longer-path
  allow or disallow matching more faithfully
- lowered `llms.txt` audit severity so the app no longer frames it like a
  universal ranking requirement
- hardened frontend session handling by using `sessionStorage` for auth tokens
  and replacing dynamic `innerHTML` paths with safer DOM construction
- expanded frontend Docker packaging so the scanner, graph, validator, and
  operator pages are present inside the shipped container
- aligned runtime, contract, and public release markers around `v6.3.0`

## Why it matters

Before `v6.3.0`, the repo was strong but still easier to criticize for:

- over-weighting experimental AI files
- script surfaces that felt less standalone than the public narrative implied
- release hygiene gaps between code, docs, and packaged UI surfaces

After `v6.3.0`, the repo is better positioned as:

- a standards-aware GEO and SEO operating system
- a more trustworthy AI-agent-ready handoff surface
- a safer self-hosted runtime foundation

## Honest boundary

`v6.3.0` still does **not** mean:

- guaranteed rankings or guaranteed AI citations
- a hosted SaaS run by the repo maintainer
- that experimental AI guidance files are official or required across every
  provider

It does mean the repo now expresses its boundaries, script surface, and current
SEO/GEO/AI guidance more honestly and more consistently.
