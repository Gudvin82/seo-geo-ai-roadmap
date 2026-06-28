# Issue Pack Workflow

`v6.8.0` добавляет lightweight issue-pack generator, чтобы быстрее переводить
аудиты в повторяемые execution packs.

## Почему это важно

У многих команд сильные findings, но слабый handoff.

Issue-pack path помогает превратить:

- audit findings
- proof gaps
- semantic gaps
- technical blockers

в reviewable implementation queue.

## Команда

```bash
python scripts/issue_pack_generator.py \
  --project example.com \
  --finding "Thin service proof|high|content_lead|expand case proof and CTA" \
  --finding "Missing FAQ schema|medium|seo_operator|add FAQPage markup and visible FAQ"
```

## Лучшее применение

- drafting GitHub Issues
- client-safe backlog handoff
- routing от agency operator к implementation-team
