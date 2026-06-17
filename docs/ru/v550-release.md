# Сводка релиза v5.5.0

`v5.5.0` превращает проект в более цельную self-hosted SaaS-ready и
multi-model operating platform, но честно не выдает его за уже работающий
maintainer-hosted SaaS.

## Что добавлено

- provider catalog, model registry, health и operating-center API surfaces
- SaaS readiness center, который показывает, что уже сильно, а что все еще
  остается вне рамок managed hosted offering
- social command center и social idea parser, который превращает raw text из
  постов и комментариев в FAQ, objections, proof и content actions
- frontend-панели для provider health, model routing, SaaS readiness и social
  parsing
- более чистая git-гигиена для generated scaffold output

## Почему это важно

- теперь можно честнее и сильнее говорить про `self-hosted SaaS-ready platform`
- оператор видит, готов ли tenant, provider и notification setup к реальной
  delivery-работе
- social layer теперь делает больше полезной работы, а не только перечисляет
  каналы
- multi-model слой стало проще объяснять, проверять и маршрутизировать

## Честная граница остается

`v5.5.0` все еще не обещает:

- maintainer-hosted public SaaS
- live billing automation
- enterprise SSO или SCIM из коробки
- тихие автономные production changes без review
