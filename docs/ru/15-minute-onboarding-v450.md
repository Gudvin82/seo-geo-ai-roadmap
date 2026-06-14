# Онбординг за 15 минут v4.5.0

Это самый быстрый и наименее фрикционный путь для нового оператора или AI
coding agent.

## Цель

Примерно за 15 минут вы должны суметь:

1. поднять стек
2. открыть приложение
3. создать workspace и project
4. подключить одного provider или остаться в starter mode
5. запустить один audit или scanner job
6. открыть один report или machine-readable artifact

## Быстрый путь

1. Клонируйте репозиторий.
2. Скопируйте `.env.example` в `.env`.
3. Выполните `make up`.
4. Выполните `make migrate`.
5. Выполните `make seed`, если нужны demo data.
6. Откройте приложение и войдите.
7. Создайте один workspace и один project.
8. Добавьте один provider config или останьтесь в прозрачном starter mode.
9. Запустите один audit или используйте scanner intake page.
10. Экспортируйте один report или task bundle.

## Если вы используете AI coding agent

Сначала дайте ему эти файлы:

- [START_HERE_FOR_AI_RU.md](../../START_HERE_FOR_AI_RU.md)
- [AGENTS.md](../../AGENTS.md)
- [DOCS_INDEX_RU.md](../../DOCS_INDEX_RU.md)

Потом дайте задачу:

`Разверни этот репозиторий, создай один project, запусти один audit и верни executive summary плюс top fixes.`

## Если вы строите client-facing scanner

Дальше идите сюда:

- [ONE_DAY_SERVICE_BLUEPRINT_RU.md](../../ONE_DAY_SERVICE_BLUEPRINT_RU.md)
- [docs/ru/integration-production-matrix-v450.md](./integration-production-matrix-v450.md)

## Почему этому пути можно доверять

В `v4.5.0` корневой и backend test path прогоняются полностью в зеленый цвет.
