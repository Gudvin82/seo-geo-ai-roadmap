# Checklist Generator

В `v6.7.5` появился практический генератор чеклистов, чтобы repo был не только
библиотекой статичных документов.

## Зачем это нужно

Разным проектам нужны разные первые действия:

- service business требует offer clarity и proof density
- local business требует maps, NAP, reviews и regional trust
- SaaS-продукт требует use-case pages, comparison intent и integration facts
- RU market требует явного разбора Yandex, Alice AI и commercial factors

Генератор дает команде повторяемый first pass, вместо того чтобы каждый раз
собирать чеклист вручную.

## Команда

```bash
python scripts/checklist_generator.py \
  --site-type service \
  --market ru \
  --focus seo \
  --focus geo \
  --focus local
```

## Что на выходе

- markdown checklist для оператора или AI-агента
- JSON payload для automation или backlog creation
- явные priority, owner и reason по каждому действию

## Когда использовать

Используйте в начале проекта, при квартальном re-baseline или перед генерацией
клиентской roadmap.
