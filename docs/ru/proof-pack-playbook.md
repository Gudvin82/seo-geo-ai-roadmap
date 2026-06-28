# Proof Pack Playbook

`v6.7.5` усиливает evidence-layer через lightweight proof-pack builder.

## Цель

Превратить улучшения в reusable, bounded и publishable artifact:

- что именно изменили
- что измерили до и после
- какие facts безопасно заявлять публично
- какие интерпретации остаются bounded inferences
- какие ссылки подтверждают claim set

## Команда

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

## Почему это важно

Репозиторий не должен опираться на размытые case claims. Proof pack помогает
держать:

- facts отдельно от interpretation
- evidence links явными
- before/after deltas видимыми
- case publication повторяемой

## Где использовать

- drafts публичных кейсов
- client-safe delivery packs
- internal experiment logs
- handoff AI-агенту, когда владельцу сайта нужен publishable summary
