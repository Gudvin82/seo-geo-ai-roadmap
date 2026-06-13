# Graph Intelligence v3.8.0

В `v3.8.0` добавлен explainable graph layer для discoverability-операций.

Это не абстрактный code graph. Это discoverability graph, который помогает
оператору, фаундеру, клиенту или AI-агенту ответить на четыре практических
вопроса:

1. что здесь есть
2. почему это важно
3. на что это влияет
4. что исправлять следующим

## Режимы

- Граф структуры сайта: homepage, разделы, money pages, hubs, кейсы и trust pages
- Граф discoverability-поверхностей: `robots.txt`, `sitemap.xml`, `llms.txt`,
  `ai.txt`, schema, FAQ и social metadata
- Граф зависимостей проблем: blockers, easy wins и последовательность fix packs
- Граф сущностей и trust: organization, services, authors, legal pages и
  внешние подтверждения

## Продуктовая поверхность

- UI: `app/frontend/graph.html`
- Логика: `app/frontend/graph.js`
- Экспорт: выгрузка JSON прямо из graph page
- Command surface: `/geo graph`

## Почему это усиливает коммерческую часть

- Продажу проще вести, когда проблему можно показать, а не только описать
- Клиентская выдача сильнее, когда видны связи между проблемами
- Фаундер быстрее понимает, где проседают trust и proof
- AI-агенты могут объяснять remediation path человеческим языком

## Рекомендуемый порядок

1. запустить `/geo audit`
2. запустить `/geo graph`
3. открыть issue dependency view
4. экспортировать graph JSON
5. приложить его к executive summary и fix pack

## Честная граница

Graph layer является explainability-надстройкой над текущей платформой. Он не
выдается за enterprise crawler или полноценную knowledge graph platform.
