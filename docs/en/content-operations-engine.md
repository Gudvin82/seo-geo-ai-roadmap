# Content Operations Engine

The Content Operations Engine turns validated demand into a governed editorial
backlog. It is not an automatic publishing system, a ranking guarantee, or a
replacement for subject-matter expertise.

## Operating Loop

1. Collect demand from operator-authorized sources such as GSC, Yandex
   Webmaster, Wordstat exports, customer language, and competitor research.
2. Cluster each topic by intent and map it to a page type.
3. Create a queue item with demand, business value, evidence strength, effort,
   owner, and required review gates.
4. Produce a brief before drafting: user need, source requirements, internal
   links, proof assets, conversion path, and factual boundaries.
5. Require factual, editorial, legal, and technical approval before publishing.
6. Verify the published page, record evidence, then review freshness and
   cannibalization on a schedule chosen by the operator.

## Build A Queue

```bash
python scripts/content_ops_queue.py \
  --file examples/content-ops-queue-example.csv \
  --default-owner content_lead
```

The score is deliberately explainable:

`0.35 demand + 0.35 business value + 0.20 evidence strength - 0.10 effort`

It prioritizes work. It does not predict rankings, traffic, leads, or AI
citations.

## Run The Full Lifecycle

```bash
python scripts/content_lifecycle.py \
  --manifest examples/content-lifecycle/manifest.json \
  --output-dir ./artifacts/content-lifecycle
```

The example joins GSC, Yandex Webmaster, Wordstat, and competitor exports,
checks the page-to-cluster registry, validates drafts, finds position 4-15
opportunities, creates a no-writeback advisor summary, and optionally renders
an editable SVG cover. Replace example exports with operator-owned data.

After an approved page is live, IndexNow can be called explicitly:

```bash
INDEXNOW_KEY=replace-me python scripts/indexnow_submit.py \
  --host example.com \
  --url https://example.com/new-page \
  --verify
```

IndexNow acceptance and URL availability do not prove indexing or rankings.

## Mandatory Gates

- Intent and audience review
- Source and factual-claim review
- Internal-link and canonical review
- Editorial and legal approval
- Post-publish verification

## RU Operating Notes

Use Wordstat and Yandex Webmaster only through authorized exports or
operator-owned credentials. Treat regional wording, legal claims, prices, and
Yandex/Alice surfaces as review inputs, not instructions to manufacture pages.

## Boundaries

- Never bulk-publish generated text without human approval.
- Do not use competitor pages as a rewriting source.
- Do not optimize for word count alone.
- Keep a factual-source record for material claims.
- Use the existing freshness and fact-drift checks after publication.

## Related Tools

- `scripts/semantic_gap_mapper.py`
- `scripts/content_freshness_checker.py`
- `scripts/fact_drift_checker.py`
- `scripts/checklist_generator.py`
- `scripts/content_lifecycle.py`
- `scripts/indexnow_submit.py`
- `contracts/content-lifecycle.schema.json`
