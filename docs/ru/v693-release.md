# Сводка релиза v6.9.3

`v6.9.3` — это текущее публичное состояние репозитория.

Он делает три вещи:

- сохраняет growth-ops layer, появившийся в `v6.9.1`
- включает CI formatting fix из `v6.9.2`
- уменьшает GitHub Actions noise, ограничивая core push workflows веткой `main`

Этот релиз в первую очередь про release hygiene и operational clarity:

- active app и contract markers теперь совпадают с публичным релизом
- frontend release badges теперь указывают на `v6.9.3`
- script defaults для launch-oriented helpers теперь указывают на `v6.9.3`
- current docs теперь используют `v6.9.3` как live state
