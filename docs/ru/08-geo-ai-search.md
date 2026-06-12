# GEO и AI Search

`v3.2.0` делает GEO/AI-слой более конкретным, более измеримым, более
сценарным и более честным по отношению к волатильности AI-поверхностей.

## Три outcome-слоя

GEO/AI-работу нужно оценивать через три разных outcome-слоя:

| Outcome layer | Что это значит | Стабильные метрики | Proxy-метрики | Главный риск |
|---|---|---|---|---|
| Rankings | Классическая поисковая видимость и квалифицированный organic traffic | indexation, CWV, schema coverage, rankings, CTR | рост branded queries | попытка заменить SEO одним GEO |
| AI citations / AI visibility | Упоминают ли LLM-поверхности бренд, цитируют ли его и правильно ли его описывают | полностью стабильных метрик почти нет | AI SoV, AI Citation Score, answer-surface coverage | продажа волатильных proxy-метрик как истины |
| Conversion & trust | Превращается ли discoverability в лиды, pipeline и доверие к бренду | формы, звонки, assisted conversions | обратная связь sales, branded demand | visibility без коммерческого намерения и доверия |

## Что влияет на какой слой

| Действие | Rankings | AI visibility | Conversion & trust |
|---|---|---|---|
| Техническая SEO-гигиена | High | Medium | Medium |
| Canonical fact consistency | Medium | High | High |
| Answer-ready структура страниц | Medium | High | High |
| JSON-LD и entity clarity | High | High | Medium |
| llms.txt / доступ AI-ботов | Low | High | Low |
| Сильный оффер, proof и CTA | Medium | Medium | High |
| Согласованные внешние упоминания бренда | Medium | High | Medium |

## Минимальная программа при ограничениях

Если времени или ресурса мало:

1. Исправьте crawlability, rendering, speed, canonicalization и indexability.
2. Синхронизируйте homepage, about, service, FAQ, contacts и policy pages по
   фактам.
3. Добавьте answer-ready sections и structured data на money pages.
4. Опубликуйте `llms.txt`, проверьте robots-правила для AI-ботов и отслеживайте
   AI SoV как proxy, а не как ground truth.
5. Привяжите каждое GEO/AI-действие к бизнес-странице или к buyer journey.

## Decision tree

- Если техническая SEO-слабая, сначала чините её, а потом масштабируйте GEO.
- Если бренд цитируют, но искажают, приоритет — fact consistency и entity
  clarity.
- Если сайт понятен ботам, но слаб для людей, усиливайте proof, offer clarity и
  conversion flow.
- Если AI visibility растёт без бизнес-эффекта, пересоберите intent и
  коммерческую framing-логику страниц.

## GEO/AI execution loop

1. Зафиксируйте baseline по technical SEO и business goals.
2. Зафиксируйте baseline по AI surfaces и citation proxies.
3. Разметьте entity facts, offer clarity и answer-ready gaps.
4. Обновите ключевые страницы и structured data.
5. Отслеживайте изменения отдельно в search, AI и business слоях.
6. Помечайте выводы как observed fact, inferred issue, hypothesis или
   recommended action.

## Чего нельзя обещать

- гарантированные AI citations
- детерминированные rankings от одного `llms.txt`
- универсальный GEO-playbook для любой ниши
- “AI optimization” без technical SEO, facts и trust assets

## Связанные документы

- [geo-measurement-maturity.md](./geo-measurement-maturity.md)
- [geo-business-outcomes.md](./geo-business-outcomes.md)
- [geo-priority-maps.md](./geo-priority-maps.md)
- [geo-ai-surfaces.md](./geo-ai-surfaces.md)
- [answer-ready-patterns.md](./answer-ready-patterns.md)
- [entity-seo-and-kg.md](./entity-seo-and-kg.md)
- [geo-red-team-and-risks.md](./geo-red-team-and-risks.md)
