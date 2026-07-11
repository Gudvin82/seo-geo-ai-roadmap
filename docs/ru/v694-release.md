# Сводка релиза v6.9.4

`v6.9.4` усиливает release integrity и runtime.

## Что изменилось

- Активные markers приложения, frontend, contracts, scripts и current docs
  используют `v6.9.4`.
- Для tag-релиза появился отдельный integrity gate: он вместе проверяет `HEAD`,
  Git tag, runtime version, release notes и публичные entrypoints.
- Capability matrix генерируется из runtime registry и честно маркирует каждую
  поверхность как live read-only, operator-guided или starter/stub.
- Docker worker непрерывно обрабатывает database-backed очередь scanner: есть
  ограниченные retry и dead-letter handling после ошибки worker.
- Для GSC и Яндекс Вебмастера добавлены read-only live API adapters с
  credentials владельца. Приложение не сохраняет tokens.
- Privacy-first measurement и independent case submission стали каноническими
  документационными поверхностями.
- Calibration utility теперь считает correlation score/outcome только по
  evidence, предоставленным оператором, и маркирует маленькие выборки как
  недостаточные.

## Границы

Live connectors требуют credentials и доступа к свойству со стороны
развертывающего проект. Остальные источники остаются явно starter или
operator-guided, пока не появится соответствующий live adapter. Scoring —
проверяемый инструмент принятия решений, а не обещание позиций, трафика,
конверсий или AI citations.
