# Synthetic Cases

Synthetic cases допустимы в этом репозитории только как training или demo
artifacts.

Они полезны, когда нужно:

- показать оператору, как структурировать proof pack
- продемонстрировать формат before/after отчета
- протестировать templates и generators без выдуманных client claims

Они **не** заменяют public bounded cases.

## Правило

Каждый synthetic case должен явно говорить:

- что он synthetic
- что он нужен для operator training или demo use
- что его нельзя подавать как реальный клиентский результат

## Инструмент

```bash
python scripts/synthetic_case_builder.py \
  --name "Synthetic Legal Service Demo" \
  --market ru \
  --site-type service \
  --before-score 71 \
  --after-score 84 \
  --change "expanded answer-ready service architecture" \
  --change "added proof and regional trust blocks"
```
