# Proof Pack Playbook

`v6.7.5` strengthens the evidence layer with a lightweight proof-pack builder.

## Goal

Turn improvements into a reusable, bounded, and publishable artifact:

- what changed
- what was measured before and after
- which facts are safe to state publicly
- which interpretations are only bounded inferences
- which links support the claim set

## Command

```bash
python scripts/proof_pack_builder.py \
  --site example.com \
  --change "expanded explicit AI bot allow rules" \
  --change "removed false-positive leak finding" \
  --before-score 92 \
  --after-score 94 \
  --fact "robots.txt now explicitly allows 14/14 target AI bots" \
  --inference "AI-source eligibility should be more explicit for answer engines" \
  --evidence-link https://example.com/robots.txt
```

## Why this matters

The repository should avoid vague case claims. A proof pack helps keep:

- facts separate from interpretation
- evidence links explicit
- before/after deltas visible
- case publication repeatable

## Best use

- public case study drafts
- client-safe delivery packs
- internal experiment logs
- AI-agent handoff when a site owner asks for a publishable summary
