# Brand Fact Consistency Playbook

## Goal

Reduce hallucination and trust loss by aligning brand facts across owned
surfaces.

## Inputs

- canonical brand facts sheet
- homepage, about, service, FAQ, legal, and profile pages
- current schema and `llms.txt`

## Step sequence

1. Define canonical facts and allowed variants.
2. Audit homepage, about, service, FAQ, legal, and profile pages.
3. Mark conflicts as observed fact or inferred issue.
4. Patch content, schema, and `llms.txt`.
5. Recheck AI answers and export the evidence set.

## Expected outputs

- one approved fact sheet
- page-level mismatch log
- patched schema and `llms.txt`
- post-fix verification notes

## What to measure

- number of fact conflicts removed
- consistency between page copy and schema
- cleaner repeated AI answers across prompts

## Risks

- treating market nuance as a factual contradiction
- editing copy without updating schema or fact files
- keeping multiple unofficial brand descriptions alive

## What not to promise

- zero hallucination forever after one cleanup pass
