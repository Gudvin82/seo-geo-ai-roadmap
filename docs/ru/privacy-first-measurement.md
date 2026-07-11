# Privacy-First измерения

Этот путь используется, когда политика продукта, регулирование или доверие
посетителей не позволяют ставить сторонний browser analytics tag.

## Что можно измерять

- server access logs с минимизацией IP и зафиксированным сроком хранения
- агрегированную поисковую статистику Search Console и Яндекс Вебмастера
- согласованные CRM-события и offline conversion imports
- self-hosted cookieless analytics под контролем владельца
- synthetic performance checks и агрегированные field data CrUX

## Правила работы

1. Собирать только метрику, необходимую для решения.
2. Хранить raw logs отдельно от proof pack и ограничивать доступ операторов.
3. Маркировать источник каждой метрики: `server`, `search_console`,
   `webmaster`, `consented_crm`, `synthetic` или `field_aggregate`.
4. Не выводить личность посетителя из audit artifact.
5. Явно указывать пробелы в измерениях, а не заполнять их оценочными
   утверждениями о конверсии.

## Применение

Этот режим позволяет сопоставлять crawlability, index coverage, search demand,
landing-page quality, performance, citation readiness и подтвержденные business
outcomes. Он не заменяет исследование продуктовой аналитики с корректно
полученным согласием, если такое исследование требуется.
