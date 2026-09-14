# Калибровка scoring

GEO score - объяснимый score готовности для приоритизации. Это не прогноз
позиций, AI-цитирований, трафика, лидов или выручки.

Используйте `scripts/scoring_calibration.py` только с согласованными
датированными evidence:

```csv
case_id,heuristic_score,observed_outcome,outcome_definition,observed_at,observation_window_days,evidence_reference
site-001,62,14,organic_click_change_percent,2026-09-01,28,docs/ru/proof-pack-site-001.md
```

Начните с [шаблона](../../examples/scoring-calibration-template.csv):

```bash
python scripts/scoring_calibration.py examples/scoring-calibration-template.csv
```

Инструмент вернет `insufficient_evidence`, пока нет минимум 30 независимых
кейсов, одного сопоставимого определения outcome, датированных наблюдений и
proof reference для каждой записи. Найденная корреляция - только сигнал для
калибровки, а не доказательство причинности. Публикуйте отрицательные и
нулевые результаты рядом с положительными, сохраняйте исходные provider
exports там, где есть согласие, и сегментируйте результаты по рынку или типу
сайта до изменения весов.
