# Кейс: anmalishev.ru — public before / after после внедрения SEO + GEO + AI methodology

Date: 2026-06-14
Site: <https://anmalishev.ru/>
Methodology source: <https://github.com/Gudvin82/seo-geo-ai-roadmap>

## Короткая версия

Этот кейс показывает, как реальный публичный сайт был усилен с помощью
методологии `seo-geo-ai-roadmap` сразу на трех уровнях:

- classical SEO и crawl structure
- GEO и discoverability для российского рынка
- AI-facing visibility для LLM и answer engines

Ключевой момент: это был не косметический content refresh. Внедрение было
сосредоточено на canonical surfaces, entity clarity, trust и contact
structure, AI-facing files, Yandex AI direction и answer-ready expert pages.

## Объем работ

На `anmalishev.ru` были внедрены следующие публичные изменения:

- более сильный homepage entity и trust graph
- выделенная canonical `Contacts` page
- выделенная `Yandex AI / Neuro` page для AI visibility в российском рынке
- выделенная `AI site audit` page для audit-intent coverage
- page с обзором репозитория, связанная с публичным GitHub profile
- улучшенные `llms.txt`, `ai.txt` и `sitemap.xml`
- сохраненная доступность для AI crawlers в `robots.txt`
- более плотная внутренняя связка между homepage, expert pages, contacts и public proof surfaces

## Public current-state verification

Следующие public signals можно проверить сейчас:

- `robots.txt` доступен и оставляет major AI и search bots разрешенными, при этом защищает admin и raw-template paths
- `llms.txt` подробный и ведет на about, contacts, methodology, services, products, GEO pages и repository proof
- `ai.txt` согласован с `llms.txt` и sitemap
- `sitemap.xml` теперь включает более сильные canonical surfaces:
  - `/contacts`
  - `/projects/seo-geo-ai-roadmap.html`
  - `/expert/yandex-neuro-ai-visibility.html`
  - `/expert/ai-site-audit.html`

## Bounded before / after

Состояние “before” — это implementation record из процесса внедрения.
Состояние “after” подтверждается текущими public URLs.

| Метрика | До | После | Delta | Тип доказательства |
|---|---:|---:|---:|---|
| Public snapshot score | 79/100 | 88/100 | +9 | bounded methodology scoring |
| URLs в `sitemap.xml` | 86 | 88 | +2 | rollout record + current public sitemap |
| Non-empty lines в `llms.txt` | 55 | 58 | +3 | rollout record + current public `llms.txt` |
| `llms.txt` validation | PASS | PASS | stable | current public file |
| AI bot access в `robots.txt` | allowed baseline | allowed baseline | stable | current public file |
| Canonical contact surface | weak | present | improved | current public URL |
| Yandex AI / Neuro surface | absent | present | improved | current public URL |
| AI audit-intent surface | absent | present | improved | current public URL |
| Homepage entity и trust graph | mixed | stronger | improved | bounded structural reading |
| AI-facing architecture coherence | medium | stronger | improved | public file alignment |

## Интерпретация score

### До: 79/100

- Technical SEO и crawl readiness: `16/20`
- Factual consistency и truth-center discipline: `15/20`
- Entity clarity и trust proof: `15/20`
- AI readiness и answer extraction: `18/20`
- Reporting и operator packaging: `15/20`

### После: 88/100

- Technical SEO и crawl readiness: `18/20`
- Factual consistency и truth-center discipline: `18/20`
- Entity clarity и trust proof: `17/20`
- AI readiness и answer extraction: `20/20`
- Reporting и operator packaging: `15/20`

## Что конкретно улучшилось

### 1. Canonical surfaces стали явными

До внедрения у сайта уже была нормальная техническая база, но часть важных
intent'ов не была выражена через dedicated canonical pages.

После внедрения сайт получил:

- четкую `Contacts` page
- четкую `Yandex AI / Neuro` page
- четкую `AI site audit` page

### 2. Российский AI-слой стал явным

Сильная сторона кейса в том, что оптимизация шла не только под абстрактную
"AI visibility".

Появился отдельный российский слой вокруг:

- `Яндекс ИИ`
- `Нейро`
- answer-ready explanations
- GEO relevance для российских запросов
- entity clarity между homepage, expert pages и contacts

### 3. AI-facing files стали ближе к реальной архитектуре сайта

Методология применялась не только на уровне pages и content, но и на уровне
AI-facing architecture.

Усиленные assets:

- `llms.txt`
- `ai.txt`
- `sitemap.xml`
- согласованность с `robots.txt`

### 4. Trust и entity consistency улучшились

Homepage graph стал сильнее за счет более ясных связей между:

- person
- business
- services
- public repository
- contacts
- expert pages
- public proof surfaces

## Что остается вне public proof

Этот кейс специально не делает claims про закрытые результаты, которые не были
публично подтверждены.

Для этого все еще нужен private analytics access:

- Google Search Console impressions, clicks и CTR
- Yandex Webmaster indexing и query data
- GA4 и Yandex Metrica conversions
- Bing Webmaster visibility
- repeated AI Share of Voice prompt packs
- controlled AI citation measurement

## Честный вывод

Методология дала сильный public delta:

- лучше crawl и canonical structure
- сильнее trust и contact layer
- явное покрытие Yandex AI
- сильнее AI-facing architecture
- чище entity graph
- лучше выровнена структура сайта с discoverability goals

Публично и прозрачно сайт moved from `79/100` to `88/100` в bounded
methodology model.

Оставшийся путь до практических `9.5/10` или `10/10` — это уже в основном не
про недостающие pages, а про measurement maturity:

- GSC
- Yandex Webmaster
- GA4 или Metrica
- AI SoV tracking
- repeated citation measurement
- operator dashboards и reporting loops

## Public URLs из кейса

- <https://anmalishev.ru/>
- <https://anmalishev.ru/contacts>
- <https://anmalishev.ru/expert/yandex-neuro-ai-visibility.html>
- <https://anmalishev.ru/expert/ai-site-audit.html>
- <https://anmalishev.ru/projects/seo-geo-ai-roadmap.html>
- <https://anmalishev.ru/llms.txt>
- <https://anmalishev.ru/ai.txt>
- <https://anmalishev.ru/sitemap.xml>
