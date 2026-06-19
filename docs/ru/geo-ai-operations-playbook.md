# GEO and AI Operations Playbook

Этот playbook нужен, чтобы GEO перестал быть “интересной идеей” и стал
repeatable operating loop.

## Цикл работы

1. определить tracked entities, offers и claims
2. определить tracked prompts и answer surfaces
3. просматривать AI answers вручную или через bounded tooling
4. фиксировать factual drift, citation behavior и omission patterns
5. обновлять trust pages, facts, FAQ и answer-ready content
6. повторно прогонять и сравнивать

## Что мониторить

- mention бренда: yes or no
- наличие citation
- качество source URL
- factual accuracy
- drift claims
- присутствие competitors
- использование trust pages
- RU-specific behavior, включая YandexAdditional и Yandex Neuro surfaces

## Что чаще всего ломается

- бренд упоминается, но не цитируется
- бренд цитируется, но описывается размыто
- повторяются устаревшие факты
- слабые case-study и proof pages
- слишком тонкие FAQ и definition layers
- AI-facing files существуют, но не совпадают с реальным сайтом

## Что чинить в первую очередь

1. factual contradictions
2. отсутствие canonical trust pages
3. слабые answer-ready blocks
4. плохую связность между homepage, about, services, cases и legal pages
5. рассинхрон `robots.txt`, `llms.txt`, `ai.txt` и sitemap

## Дисциплина доказательств

Каждый GEO cycle должен сохранять:

- использованный prompt
- provider или surface
- дату
- observed answer
- citation state
- mismatch notes
- что было изменено после этого

Без этого GEO превращается в storytelling, а не в operations.

## Выходы

- AI visibility audit log
- factual drift log
- entity и trust backlog
- answer-ready content backlog
- before / after evidence pack
