# Security Advisory Baseline

This file documents the current `pip-audit` ignores used by CI in `v6.3.0`.

The goal is not to hide dependency risk. The goal is to keep the dependency
scan strict while making the remaining exceptions explicit and reviewable.

## Current ignores

### `pytest` test-only advisory

- `GHSA-6w46-j5rx-g56g`

Reason:

- `pytest` is a test dependency, not a shipped runtime dependency
- the fix version requires a newer support floor than the local Python 3.9
  environment used by this repo today

### `starlette` transitive advisories

- `PYSEC-2026-161`
- `PYSEC-2026-249`
- `PYSEC-2026-248`
- `GHSA-7f5h-v6xp-fcq8`
- `GHSA-wqp7-x3pw-xc5r`
- `GHSA-x746-7m8f-x49c`

Reason:

- `starlette` is currently constrained by the active FastAPI support matrix in
  this repository
- a clean upgrade path should be taken together with a deliberate Python and
  FastAPI support-floor move, not as an unreviewed patch during a release pass

## Review rule

These ignores are not permanent.

On the next framework support-floor upgrade, re-run:

```bash
pip-audit -r app/backend/requirements.txt
```

and remove any ignore that is no longer needed.
