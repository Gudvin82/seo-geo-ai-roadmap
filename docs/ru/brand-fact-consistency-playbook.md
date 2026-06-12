# Brand Fact Consistency Playbook

## Цель

Снизить hallucination и trust loss через выравнивание brand facts на собственных
поверхностях.

## Inputs

- canonical brand facts sheet
- homepage, about, service, FAQ, legal и profile pages
- текущие schema и `llms.txt`

## Последовательность шагов

1. Определите canonical facts и допустимые variants.
2. Аудируйте homepage, about, service, FAQ, legal и profile pages.
3. Помечайте конфликты как observed fact или inferred issue.
4. Обновляйте контент, schema и `llms.txt`.
5. Перепроверяйте AI answers и экспортируйте evidence set.

## Ожидаемые outputs

- один утверждённый fact sheet
- page-level mismatch log
- обновлённые schema и `llms.txt`
- post-fix verification notes

## Что измерять

- количество устранённых fact conflicts
- согласованность между page copy и schema
- более чистые повторяющиеся AI answers по разным prompts

## Риски

- путать рыночную адаптацию с factual contradiction
- править copy без обновления schema или fact files
- держать в обороте несколько неофициальных описаний бренда

## Чего не обещать

- нулевую hallucination forever после одного cleanup pass
