# Security Advisory Baseline

Этот файл документирует текущие `pip-audit` ignores, которые используются в CI
начиная с `v6.3.0`.

Цель не в том, чтобы скрыть dependency risk. Цель в том, чтобы dependency scan
оставался строгим, а исключения были явными и ревьюируемыми.

## Текущие ignores

### `pytest` test-only advisory

- `GHSA-6w46-j5rx-g56g`

Причина:

- `pytest` — это test dependency, а не shipped runtime dependency
- фиксирующая версия требует более нового support floor, чем локальная Python
  3.9 среда, на которую repo все еще опирается сегодня

### `starlette` transitive advisories

- `PYSEC-2026-161`
- `PYSEC-2026-249`
- `PYSEC-2026-248`
- `GHSA-7f5h-v6xp-fcq8`
- `GHSA-wqp7-x3pw-xc5r`
- `GHSA-x746-7m8f-x49c`

Причина:

- `starlette` сейчас ограничен активной FastAPI support matrix этого
  репозитория
- clean upgrade path нужно делать вместе с осознанным повышением Python и
  FastAPI support floor, а не как непроверенный patch внутри релизной проходки

## Правило пересмотра

Эти ignores не являются постоянными.

При следующем upgrade framework support floor надо заново прогнать:

```bash
pip-audit -r app/backend/requirements.txt
```

и удалить все ignore, которые больше не нужны.
