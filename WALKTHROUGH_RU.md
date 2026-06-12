# Пошаговый Разбор

## Идеальный первый проход

Это самый короткий proof-first путь по проекту.

1. Прочитайте [README_RU.md](./README_RU.md)
2. Выполните `make turnkey-demo`
3. Откройте `http://localhost:3000`
4. Войдите через `demo@example.com / DemoPlatform123`
5. Откройте обзорную панель
6. Выберите demo workspace и project
7. Откройте reports и artifacts
8. Запустите свежий audit
9. Запустите AI SoV
10. Экспортируйте project package

## Что вы должны увидеть

- рабочий login flow
- один workspace и один project
- видимую историю аудитов
- видимый слой reports и artifacts
- prompt library и notification endpoints
- историю AI SoV с прозрачными заметками

## После первого видимого результата

1. Замените demo site на реальный project
2. Заполните свои brand facts
3. Подключите cloud или local providers
4. Запустите первый реальный audit
5. Превратите findings в fix backlog
6. Повторно прогоните после изменений и сравните дельты

## Путь человека и путь ИИ

- Путь human operator: этот walkthrough плюс [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)
- Путь AI agent: [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md) плюс
  [AGENTS.md](./AGENTS.md)

## Proof assets

![Login and dashboard proof](./docs_site/assets/screenshots/app-login-dashboard-proof.png)
![Provider configuration proof](./docs_site/assets/screenshots/app-provider-proof.png)
![Audit run proof](./docs_site/assets/screenshots/app-audit-proof.png)
![Report and artifact proof](./docs_site/assets/screenshots/app-report-proof.png)
