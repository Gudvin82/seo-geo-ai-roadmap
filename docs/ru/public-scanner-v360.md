# Public Scanner Foundation

`v3.6.0` добавляет self-hosted/public-ready scanner foundation поверх
существующего app и audit flow.

## Что входит в этот foundation

- dedicated intake page для passive, active и full scan modes
- безопасная нормализация URL и SSRF-oriented блокировка target-адресов
- ownership verification для active и full scan modes
- consent recording для passive и active scan path
- async scan jobs со статусом, events и artifacts
- optional webhook, SMTP/email и Telegram completion hooks

## Режимы развертывания

- Local dev:
  только для разработки и UI-тестов
- Self-hosted internal:
  для operator-only или agency-internal deployment
- Self-hosted public intake:
  открывать intake page только при настроенных reverse proxy, rate limiting,
  logging и safe feature flags

## Feature flags

Опасное поведение выключено по умолчанию:

- `ALLOW_PUBLIC_INTAKE=false`
- `ALLOW_ACTIVE_SCAN=false`
- `ALLOW_ANONYMOUS_SUBMISSION=false`
- `ALLOW_FULL_SCAN=false`

Дополнительные scanner controls:

- `SCANNER_ALLOWED_SCHEMES`
- `SCANNER_MAX_URL_LENGTH`
- `SCANNER_MAX_CONCURRENT_SUBMISSIONS_PER_IP`
- `SCANNER_VERIFICATION_TTL_MINUTES`
- `SCANNER_WEBHOOK_TIMEOUT_SECONDS`

## Краткий threat model

Этот релиз не выдает себя за hardened multi-tenant public SaaS. Это безопасный
self-hosted foundation.

Основные угрозы, учтенные в `v3.6.0`:

- SSRF в локальные, private или metadata targets
- неавторизованный active scanning сторонних доменов
- неограниченный public intake без feature flags
- long-running jobs без видимого lifecycle
- report delivery без schema и event trail

## Abuse boundaries

- localhost, RFC1918, loopback, link-local, reserved и metadata-style targets
  блокируются
- active и full scans требуют ownership verification и explicit consent
- submissions throttled по IP и по domain
- dangerous modes остаются feature-flagged

## Reverse proxy и rate-limit guidance

Для public intake рекомендуется:

- завершать TLS на reverse proxy
- включать request rate limiting per IP
- ограничивать размер request body
- корректно прокидывать `X-Forwarded-For`
- держать app access logs и reverse-proxy logs согласованными

## Storage и retention

- verification records, consent records, scan jobs и scan events хранятся в
  application database
- generated artifacts хранятся под configured artifact root
- до включения high-volume public intake нужно определить cleanup policy

## Privacy notice template

Рекомендуемое уведомление оператора:

> Этот self-hosted scanner хранит submitted URLs, verification records, consent
> confirmations, job events и generated artifacts для operational и audit
> purposes.

## Responsible use statement

- не использовать scanner как замену penetration testing
- не запускать active scans без ownership или explicit authorization
- трактовать heuristic outputs как operator input, а не как legal/security guarantee
