# Security Checklist

## Аутентификация и пароли

- Пароли хешируются через Argon2id, а не через простой SHA-256.
- Во всех non-local средах используйте сильный `APP_SECRET_KEY`.
- Сохраняйте минимальную password policy:
  - минимум 12 символов
  - uppercase
  - lowercase
  - цифры
- Никогда не используйте demo credentials в реальном проде.

## Жизненный цикл токенов

- Access tokens должны истекать.
- Перед production rollout проверьте `APP_TOKEN_TTL_MINUTES`.
- При sign-out токены должны отзываться.
- Не используйте бессрочные bearer tokens.

## Защита от brute-force

- Не отключайте окно login-attempt защиты.
- Проверьте `APP_LOGIN_ATTEMPT_LIMIT`.
- Проверьте `APP_LOGIN_ATTEMPT_WINDOW_SECONDS`.
- В production ставьте приложение за reverse proxy или edge rate limiter.

## Секреты и provider keys

- Никогда не коммитьте реальные provider API keys.
- Храните ключи в environment variables или secret manager.
- После инцидентов и смены команды ротируйте credentials.
- Ограничивайте круг людей, которые могут видеть deployment secrets.

## База данных и инфраструктурная гигиена

- Обязательно заменяйте sample database passwords.
- Используйте отдельного database user для приложения.
- Настройте backups для PostgreSQL volume или managed instance.
- Ограничьте прямой доступ к базе доверенными операторами.

## HTTPS и reverse proxy

- Терминируйте HTTPS через Nginx, Caddy, Traefik или managed load balancer.
- Не публикуйте production-приложение по обычному HTTP.
- Держите forwarded headers и origin settings в соответствии с реальным deployment.

## Workspace isolation и артефакты

- Проверяйте, что каждый user видит только свои workspaces и projects.
- Контролируйте права доступа к artifact storage.
- Если отчеты и артефакты важны бизнесу, включите их резервное копирование.

## Поддержка зависимостей и платформы

- Регулярно обновляйте Python dependencies.
- После обновлений зависимостей прогоняйте тесты.
- Следите за security advisory у используемых framework.
- Перед production-upgrade проверяйте изменения в provider API.

## CI security checks в `v3.3.0`

- `pip-audit` запускается в GitHub Actions по `app/backend/requirements.txt`.
- `gitleaks` запускается в GitHub Actions и ищет вероятные секреты в репозитории.
- Python CI теперь генерирует coverage artifact, чтобы reviewer мог проверить test reach по critical-path логике.

## Что эти проверки не гарантируют

- Они не заменяют ручной review auth, permissions и business-logic risks.
- Они не гарантируют безопасность сторонних endpoints.
- Они не превращают репозиторий в managed security service.
