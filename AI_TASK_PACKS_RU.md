# AI Task Packs

Используйте этот файл, когда хотите, чтобы AI coding agent делал реальную
работу, а не угадывал, какой prompt ему лучше дать.

Эти task packs специально сделаны:

- explicit
- approval-first
- честно в границах того, что репозиторий реально умеет сегодня

## Pack 1. Аудит сайта по методологии репозитория

Подходит, когда:

- нужен bounded SEO + GEO + AI аудит
- нужен client-ready report
- важно, чтобы AI использовал repo-native scripts, а не придумывал свой фреймворк

Сначала прочитать:

1. [START_HERE_FOR_AI_RU.md](./START_HERE_FOR_AI_RU.md)
2. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
3. [REAL_CASES_RU.md](./REAL_CASES_RU.md)

Prompt:

```text
Используй этот репозиторий как operating framework:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Задача:
1. Сначала оцени сам репозиторий, чтобы не overclaim what it does.
2. Затем проведи аудит этого сайта по методологии репозитория: {{TARGET_URL}}
3. По возможности используй repo-native scripts, docs и scoring logic.
4. Разделяй:
   - verified observations
   - heuristic findings
   - assumptions
5. Выдай:
   - executive summary
   - score breakdown
   - strongest positives
   - top weaknesses
   - prioritized actions по impact, effort, confidence
   - quick wins на 7 дней
   - deeper fixes на 30 дней
   - что можно внедрять только после human approval
6. Если script result конфликтует с видимой реальностью сайта, объясни вероятную причину.
7. Заверши client-safe report и operator backlog.
```

## Pack 2. Развернуть платформу локально или на сервере

Подходит, когда:

- нужен self-hosted stack
- нужен demo или internal operator install
- нужно, чтобы AI остановился на безопасном и проверяемом deployment

Сначала прочитать:

1. [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
2. [ONE_CLICK_DEPLOY_OPTIONS_RU.md](./ONE_CLICK_DEPLOY_OPTIONS_RU.md)
3. [DEPLOYMENT_RU.md](./DEPLOYMENT_RU.md)

Prompt:

```text
Используй этот репозиторий как базу:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Задача:
1. Разверни репозиторий самым быстрым безопасным self-hosted способом.
2. Держи честную public promise:
   - self-hosted
   - open-source
   - AI-agent-ready
   - foundation для scanner или audit service
3. Настрой:
   - app stack
   - login
   - workspace
   - один demo project
   - scanner intake
   - report export
4. Проверь:
   - frontend открывается
   - API docs открываются
   - demo login работает
   - один audit path работает
5. Верни:
   - deployment URL
   - credentials
   - что production-ready
   - что еще требует operator setup
   - exact next steps
```

## Pack 3. Улучшить существующий сайт после утверждения аудита

Подходит, когда:

- аудит уже есть
- нужен implementation planning или execution
- изменения должны оставаться контролируемыми

Сначала прочитать:

1. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)
2. [docs/ru/technical-seo-deep-playbook.md](./docs/ru/technical-seo-deep-playbook.md)
3. [docs/ru/geo-ai-operations-playbook.md](./docs/ru/geo-ai-operations-playbook.md)

Prompt:

```text
Используй этот репозиторий как framework:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Задача:
1. Просмотри существующие audit findings по {{TARGET_URL}}.
2. Раздели работу на:
   - quick wins
   - medium effort changes
   - strategic architecture work
3. Приоритизируй по impact, effort, confidence и proof level.
4. Подготовь:
   - implementation backlog
   - page-level change plan
   - schema / facts / FAQ / technical fixes
   - approval gates before deployment
5. Не публикуй рискованные изменения silently.
6. Если есть доступ, после approval подготовь patches или implementation-ready payloads.
```

## Pack 4. Превратить репозиторий в основу клиентского сервиса

Подходит, когда:

- нужен branded scanner или audit service
- нужен deployment плюс operating boundaries
- нужна честная SaaS-подача

Сначала прочитать:

1. [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
2. [ONE_DAY_SERVICE_BLUEPRINT_RU.md](./ONE_DAY_SERVICE_BLUEPRINT_RU.md)
3. [BUILD_WITH_THIS_PLATFORM_RU.md](./BUILD_WITH_THIS_PLATFORM_RU.md)

Prompt:

```text
Используй этот репозиторий как базу для branded scanner или audit service.

Задача:
1. Считай репозиторий self-hosted foundation, а не finished hosted SaaS.
2. Предложи safest branded setup для:
   - intake
   - audit workflow
   - reporting
   - task export
   - operator review
3. Настрой один demo workspace и один demo project.
4. Покажи, что еще нужно для:
   - public intake
   - abuse control
   - queue policy
   - notifications
   - tenant operations
5. Верни:
   - architecture summary
   - deployment path
   - client-safe promise
   - missing layers до hosted-SaaS maturity
```

## Pack 5. Честно оценить репозиторий перед публичным постом

Подходит, когда:

- вы хотите выпустить пост или launch note
- нужно, чтобы AI challenged overclaiming
- нужен reality check

Сначала прочитать:

1. [PUBLIC_PRODUCT_READINESS_RU.md](./PUBLIC_PRODUCT_READINESS_RU.md)
2. [METHODOLOGY_RU.md](./METHODOLOGY_RU.md)
3. [SCORING_EXPLAINED_RU.md](./SCORING_EXPLAINED_RU.md)

Prompt:

```text
Оцени этот репозиторий как skeptical but fair evaluator.

Задача:
1. Раздели, что здесь:
   - production-ready today
   - strong but foundation-level
   - still starter or scaffold
2. Найди формулировки в моем публичном посте, которые overclaim the repo.
3. Перепиши пост так, чтобы он оставался сильным, но был полностью честным.
4. Объясни, что о нем подумают SEO-специалист, разработчик, фаундер и AI-агент.
5. Заверши:
   - safe public wording
   - risky wording to avoid
   - next three improvements that will increase trust fastest
```
