# Prompt Для AI: Оценка Репозитория И Сайта

Используйте этот prompt, когда передаете репозиторий AI coding agent и хотите
получить реальный bounded audit, а не общую болтовню.

```text
Используй этот репозиторий как operating framework:
https://github.com/Gudvin82/seo-geo-ai-roadmap

Задача:
1. Сначала оцени сам репозиторий, чтобы не переобещать его возможности.
2. Перед аудитом прочитай:
   - README_RU.md
   - PUBLIC_PRODUCT_READINESS_RU.md
   - METHODOLOGY_RU.md
   - SCORING_EXPLAINED_RU.md
   - REAL_CASES_RU.md
3. Затем оцени этот сайт по методологии репозитория: {{TARGET_URL}}
4. Сфокусируйся на:
   - technical SEO
   - semantics и intent
   - GEO и AI discoverability
   - factual consistency
   - AI-bot access
   - schema
   - answer-readiness
   - entity и trust surfaces
5. Предпочитай repository-native scripts и docs там, где это возможно.
6. Отдельно разделяй:
   - verified findings
   - heuristic findings
   - assumptions
7. Подготовь:
   - executive summary
   - разбивку score
   - сильные стороны
   - главные слабые места
   - приоритизированный план улучшений по impact, effort, confidence
   - quick wins на 7 дней
   - deeper fixes на 30 дней
   - что проверено реально, а что является heuristic
   - что требует human approval до внедрения
8. Если script output конфликтует с видимой реальностью сайта, объясни вероятную причину.
9. Если делаешь assumptions, укажи их явно.
10. В конце выдай:
   - client-ready отчет
   - operator backlog
```
