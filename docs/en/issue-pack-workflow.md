# Issue Pack Workflow

`v6.8.0` adds a lightweight issue-pack generator so audits can be translated
into repeatable execution packs faster.

## Why it matters

Many teams have strong findings but weak handoff.

The issue-pack path helps convert:

- audit findings
- proof gaps
- semantic gaps
- technical blockers

into a reviewable implementation queue.

## Command

```bash
python scripts/issue_pack_generator.py \
  --project example.com \
  --finding "Thin service proof|high|content_lead|expand case proof and CTA" \
  --finding "Missing FAQ schema|medium|seo_operator|add FAQPage markup and visible FAQ"
```

## Best use

- GitHub Issues drafting
- client-safe backlog handoff
- agency operator to implementation-team routing
