# Сводка релиза v6.12.0

`v6.12.0` — релиз интеграции и runtime-hardening. Он не заявляет новых
детерминированных GEO-факторов, позиций или AI citations.

## Сделано

- Единый Finding/Evidence contract для новых findings, reports, task bundles,
  graph-compatible views и сохраненных proof records.
- Завершенный audit теперь может сформировать GEO runtime artifact с отдельными
  entity, citation, authority и competitor analyzer outputs.
- Score profiles валидируют weights, содержат версию и calibration status, а
  при отсутствии данных возвращают `insufficient_data`, а не искусственный ноль.
- AI visibility snapshots сохраняют query, provider, model, время, provenance
  evidence, response reference и сравнение истории.
- Agent Audit Pack доступен как executable contract с tools, limits, sequence
  и approval gates.

## Границы

- Provider-derived evidence остается provider-derived; heuristic evidence не
  доказывает AI citations, rankings, traffic или conversions.
- Runtime approval-bound и не делает автоматический CMS writeback.
- Исторические audit records поддерживаются через legacy adapter.
