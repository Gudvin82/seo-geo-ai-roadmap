# Checklist Generator

`v6.7.5` adds a practical checklist generator so the repository is not only a
library of static docs.

## Why this matters

Different projects need different first actions:

- a service business needs offer clarity and proof density
- a local business needs maps, NAP, reviews, and regional trust
- a SaaS product needs use-case pages, comparison intent, and integration facts
- the RU market needs explicit Yandex, Alice AI, and commercial-factor review

The generator gives teams a repeatable first pass instead of making every
operator assemble a checklist from scratch.

## Command

```bash
python scripts/checklist_generator.py \
  --site-type service \
  --market ru \
  --focus seo \
  --focus geo \
  --focus local
```

## Output

- markdown checklist for operators or AI agents
- JSON payload for automation or backlog creation
- explicit priority, owner, and reason per action

## Best use

Use it at the start of a project, quarterly re-baselines, or before generating a
client-facing roadmap.
