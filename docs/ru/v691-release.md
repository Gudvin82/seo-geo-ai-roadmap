# Сводка релиза v6.9.1

`v6.9.1` добавляет growth-ops layer поверх `v6.9.0`.

Что изменилось:

- conversion ops стали first-class surface в repo и app
- content architecture и programmatic SEO planning стали более явными
- customer-research и comparison work получили отдельный operator pack
- launch packaging стало безопаснее и удобнее для повторного использования в
  публичных анонсах

Новые скрипты:

- `scripts/conversion_ops_pack.py`
- `scripts/content_growth_ops.py`
- `scripts/customer_research_pack.py`
- `scripts/launch_ops_pack.py`

Новые app settings centers:

- `conversion-ops-center`
- `content-growth-center`
- `research-ops-center`
- `launch-ops-center`
