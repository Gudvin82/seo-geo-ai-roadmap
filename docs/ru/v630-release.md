# Сводка релиза v6.3.0

`v6.3.0` — это релиз, который сильнее сближает публичную методологию, runtime
behavior и repo-level execution.

## Что изменилось

- откалибрована текущая GEO и AI guidance так, что:
  - `llms.txt` рассматривается как optional AI-routing surface
  - `reasoning.json` и `.well-known/ai-manifest.json` рассматриваются как
    experimental extras
  - visible structure, schema и answer-ready content важнее, чем спорные файлы
- в модель AI-ботов добавлен `OAI-SearchBot`
- улучшена оценка `robots.txt`, чтобы корректнее обрабатывались multi-agent
  groups и longest-path allow/disallow matching
- понижена severity для `llms.txt`, чтобы приложение не трактовало его как
  универсальное ranking requirement
- frontend session handling усилен переходом на `sessionStorage` для auth tokens
  и заменой рискованных `innerHTML` путей на более безопасную DOM-construction
- frontend Docker package расширен так, чтобы scanner, graph, validator и
  operator pages реально попадали в контейнер
- runtime, contract и public release markers выровнены вокруг `v6.3.0`

## Почему это важно

До `v6.3.0` repo был сильным, но его все еще было проще критиковать за:

- переоценку experimental AI files
- script surfaces, которые ощущались менее standalone, чем обещал public
  narrative
- release hygiene разрывы между code, docs и packaged UI surfaces

После `v6.3.0` repo лучше позиционируется как:

- standards-aware GEO и SEO operating system
- более trustworthy handoff surface для AI-агентов
- более безопасная self-hosted runtime foundation

## Честная граница

`v6.3.0` все еще **не** означает:

- гарантированные позиции или гарантированные AI citations
- hosted SaaS от автора репозитория
- что experimental AI guidance files стали официальными или обязательными для
  всех провайдеров

Но это означает, что repo теперь честнее и последовательнее выражает свои
границы, script surface и текущую SEO/GEO/AI guidance.
