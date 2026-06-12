# Measurement Maturity для GEO

## Лестница надёжности

| Класс метрик | Примеры | Надёжность | Как о них говорить |
|---|---|---|---|
| Надёжные операционные метрики | crawlability, CWV, indexation, schema coverage | High | использовать как decision-grade |
| Search performance metrics | rankings, impressions, CTR, landing-page clicks | Medium to high | объяснять сезонность и query mix |
| GEO/AI proxy metrics | AI SoV, AI Citation Score, answer-surface coverage | Medium to low | считать proxy, а не гарантиями |
| Экспериментальные сигналы | prompt win-rate snapshots, разовые citation counts | Low | использовать для исследования, не для executive truth |

## Дисциплина по метрикам

| Метрика | Стабильность | Главное ограничение | Безопасная формулировка |
|---|---|---|---|
| Technical SEO issues | Stable | сами по себе не объясняют business impact | `observed issue` |
| Core Web Vitals | Stable enough | field data может запаздывать | “надёжный web-performance signal” |
| Schema coverage | Stable | покрытие не гарантирует rich results или citations | “implementation signal” |
| AI SoV | Volatile | зависит от prompt-формулировок, vendor behavior и свежести данных | “directional visibility proxy” |
| AI Citation Score | Volatile | зависит от конкретной answer surface и логики attribution | “прозрачный proxy по текущим наблюдаемым ответам” |

## Маркировка выводов

Используйте в отчётах метки:

- `observed_fact`
- `inferred_issue`
- `hypothesis`
- `recommended_action`

## Anti-hype правило

Нельзя продавать AI visibility метрики как:

- гарантированный спрос
- гарантированный рост лидов
- стабильный benchmark на всех LLM сразу
- замену analytics или CRM evidence
