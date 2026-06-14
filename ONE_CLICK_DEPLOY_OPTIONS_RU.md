# One-Click Deploy Options

Этот файл собирает самые простые пути развертывания для команд, которым нужен
быстрый результат.

Это не магические "кнопки от одного вендора".
Это самые быстрые практические маршруты, которые уже поддерживаются структурой
репозитория.

## Самый быстрый локальный proof

Используйте это, если нужен самый короткий путь к рабочему demo:

1. `cp .env.example .env`
1. `make turnkey-demo`
1. откройте `http://localhost:3000`

Лучше всего подходит для:

- доказать, что репозиторий реально работает
- показать приложение клиенту или коллеге
- проверить AI-agent handoff

## Docker VPS

Используйте это, если вам нужен самый прямой self-hosted production-like путь:

1. поднимите Linux VPS
1. установите Docker и Docker Compose
1. склонируйте репозиторий
1. настройте `.env`
1. выполните `docker compose up --build -d`
1. поставьте поверх Caddy, Nginx или Traefik

Лучше всего подходит для:

- агентств
- консультантов
- фаундеров
- команд, которым нужен полный контроль

## Coolify

Используйте это, если хотите более простой self-hosted PaaS-опыт на своем
сервере:

1. установите Coolify на свой сервер
1. подключите GitHub repo
1. создайте services для frontend, backend и PostgreSQL
1. перенесите те же env vars из `.env.example`
1. выполните migrations до подачи трафика

Лучше всего подходит для:

- команд, которым нужен более удобный app lifecycle management
- пользователей, которые хотят self-hosted ownership

## Railway

Используйте это, если хотите быстрый managed deployment flow:

1. подключите repo к Railway
1. разделите backend и frontend services
1. подключите PostgreSQL
1. задайте environment variables
1. опубликуйте frontend и backend routes
1. выполняйте migrations во время release

Лучше всего подходит для:

- быстрого proof-of-concept
- внутреннего деплоя
- команд, которым комфортен managed runtime

## Render

Используйте это, если хотите похожий managed path с понятным разделением
services:

1. подключите repo к Render
1. создайте web service для backend
1. создайте static или web service для frontend
1. подключите PostgreSQL
1. задайте environment variables и build commands
1. выполните migrations до первого публичного трафика

Лучше всего подходит для:

- low-friction proof
- небольших production rollouts
- команд, которым нужен более простой hosted ops layer

## Kubernetes pack

Используйте это, если у вас уже есть managed Kubernetes:

- DigitalOcean Kubernetes
- GKE
- EKS

В репозитории уже лежат starter manifests в `infra/k8s/`.

Лучше всего подходит для:

- команд с существующей cluster operations практикой
- multi-service или compliance-minded deployment

## Какой вариант выбрать

- самый быстрый demo: `make turnkey-demo`
- самый быстрый self-hosted server: Docker VPS
- самый удобный self-hosted panel: Coolify
- самый быстрый managed proof: Railway или Render
- existing enterprise infra: Kubernetes pack

## Минимальный launch checklist

1. проверить `.env` secrets
1. выполнить migrations
1. проверить frontend
1. проверить API docs
1. проверить login
1. проверить один audit run
1. проверить один export
1. проверить scanner intake, если он открыт публично

## Важная граница

Все эти варианты поддерживают:

- self-hosted deployment
- deployment product foundation
- deployment scanner или audit-сервиса под вашим контролем

Они не превращают репозиторий автоматически в:

- hosted SaaS от автора репозитория
- automatic enterprise support contract
- public multi-tenant service без review и настройки
