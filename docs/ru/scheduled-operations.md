# Регулярные Операции

## Какие проверки можно повторять

`v3.3.0` формализует регулярный запуск для:

- AI Share of Voice checks
- аудитов
- `llms.txt`, robots, schema и других структурных проверок

## Режимы scheduling

- internal metadata only: полезно для планирования и видимости в приложении
- cron-compatible CLI: запуск скриптов через local cron, systemd timers или worker host
- GitHub Actions schedule: подходит для repo-driven public validation и легких проверок

## Примеры расписаний

- еженедельная проверка `llms.txt`: понедельник, 09:00
- еженедельный AI visibility snapshot: вторник, 10:00
- ежемесячный full audit: первый рабочий день месяца

## Какие артефакты ожидаются

- audit logs
- reports или patch packs
- CLI JSON output для автоматизаций
- notification events, если они настроены

## Честные ограничения

- self-hosted инсталляциям все равно нужен cron, Actions или другой scheduler
- `v3.3.0` не является полноценным queue scheduler с worker leasing
- даже регулярные джобы должны проходить human review, прежде чем считать их business truth
