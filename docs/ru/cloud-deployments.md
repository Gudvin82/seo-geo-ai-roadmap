# Опциональные cloud deployment notes

Платформа остается self-hosted first. Cloud-примеры здесь нужны как ускорители, а не как обязательное условие.

## Railway

- Разверните backend-контейнер.
- Подключите PostgreSQL и задайте `APP_DATABASE_URL`.
- Установите `APP_AUTO_CREATE_SCHEMA=false`.
- Выполняйте `alembic upgrade head` при релизе или startup scripting.

## Fly.io / Render-подобный deployment

- При необходимости разносите frontend и backend по разным сервисам.
- Храните provider keys и app secrets в platform secrets.
- Если отчеты должны жить долго, вынесите artifact storage или подключите persistent volume.
