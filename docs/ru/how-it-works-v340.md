# How It Works

`v3.4.0` делает репозиторий проще в эксплуатации за счет более ясного modular
flow.

## Flow

1. Поднять стек или выбрать уже работающую среду.
2. Выбрать command surface: `audit`, `llmstxt`, `report`, `compare` и так далее.
3. Через command catalog перейти к нужным scripts, docs и API entrypoints.
4. Прогнать проверки, собрать evidence и сгенерировать reports или delivery packs.
5. Если работа становится регулярной, подключить repeated runs.

## Основные модули

- bootstrap и deployment
- routing и command surface
- scripts и validators
- backend API и audit logs
- frontend operator console
- docs, templates и delivery artifacts

## Почему это важно

Репозиторий проще оценивать и внедрять, когда первый шаг очевиден.
