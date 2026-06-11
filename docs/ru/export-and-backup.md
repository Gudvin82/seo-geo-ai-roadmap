# Export and Backup

## Что нужно бэкапить

- базу данных
- artifact storage
- `.env` и provider references
- brand facts и project metadata

## Что уже можно экспортировать

- reports
- artifacts
- provider config templates
- demo dataset через seed flow

## Путь восстановления

1. восстановить базу данных
1. восстановить artifact storage
1. вернуть `.env`
1. применить migrations, если версия окружения изменилась
