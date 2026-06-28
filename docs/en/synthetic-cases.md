# Synthetic Cases

Synthetic cases are allowed in this repository only as training or demo
artifacts.

They are useful when you want to:

- teach operators how to structure a proof pack
- demonstrate before/after reporting format
- test templates and generators without inventing fake client claims

They are **not** a replacement for public bounded cases.

## Rule

Every synthetic case must say clearly:

- that it is synthetic
- that it is for operator training or demo use
- that it should not be presented as a real client result

## Tool

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
