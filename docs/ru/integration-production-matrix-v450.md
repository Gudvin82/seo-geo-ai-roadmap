# Матрица production-flow интеграций v4.5.x

Это самый короткий операционный вид на integration layer.

## Текущие first-class интеграции

| Интеграция | Слой | Статус контракта | Поверхность proof | Лучший следующий шаг |
| --- | --- | --- | --- | --- |
| GSC | search visibility | `production_guided` | env-aware verification matrix | подключить service account и поставить recurring sync |
| GA4 | outcomes и engagement | `production_guided` | env-aware verification matrix | провалидировать baseline и использовать его в executive mode |
| Google Ads | paid search demand | `production_guided` | env-aware verification matrix | подключить credentials и сравнивать brand/non-brand demand с GSC и GA4 |
| Yandex Webmaster | RU search visibility | `production_guided` | env-aware verification matrix | подключить token и держать его в одном compare loop с GSC |
| Yandex Metrica | RU analytics | `production_guided` | env-aware verification matrix | связать с Webmaster для RU diagnostics и conversion context |
| Yandex Direct | RU paid demand и landing alignment | `production_guided` | env-aware verification matrix | подключить token и сравнивать spend и demand shifts с organic и AI visibility |
| CrUX | field data | `production_guided` | env-aware verification matrix | совместить real-user CWV с synthetic checks и CI gating |
| IndexNow | fast indexation signal | `production_guided` | env-aware verification matrix | настроить push path для свежих URL |
| Google Business Profile | local trust и maps demand | `production_guided` | env-aware verification matrix | подключить профиль и отслеживать local actions |
| Yandex Business | RU local trust и maps demand | `production_guided` | env-aware verification matrix | подключить профиль и сравнивать с RU local landing performance |
| Merchant Center | commerce feed health | `production_guided` | env-aware verification matrix | отслеживать approvals и product feed issues |
| Meta Ads | paid distribution | `distribution_guided` | env-aware verification matrix | использовать как amplification и remarketing context |
| VK Ads | RU paid distribution | `distribution_guided` | env-aware verification matrix | сравнивать с RU search demand и conversions |
| Telegram ads или channel analytics | community distribution | `distribution_guided` | env-aware verification matrix | использовать для проверки channel demand |
| YouTube Analytics | media distribution | `distribution_guided` | env-aware verification matrix | сравнивать video demand с branded search и site clicks |
| LinkedIn Ads | B2B paid distribution | `distribution_guided` | env-aware verification matrix | использовать для B2B demand amplification |
| Instagram или Facebook organic | social distribution | `distribution_guided` | env-aware verification matrix | использовать как supporting distribution signal |
| WordPress | governed CMS | `production_guided` | CMS contract плюс inventory flow | перейти от inventory к reviewed patch bundles |
| Webflow | governed CMS | `production_guided` | CMS contract плюс export-first flow | держать publish за review |
| Bitrix | governed CMS | `production_guided` | CMS contract плюс mapping validation | валидировать field mapping до automation |
| Tilda | governed CMS | `production_guided` | CMS contract плюс manual-apply flow | воспринимать как delivery path с re-audit |

## Что изменилось в v4.5.x

- integration verification layer теперь показывает required, present и missing
  environment variables
- readiness может отображать `configured` по live env state, а не только по
  статическому row metadata
- scanner, dashboard и CI-oriented flows теперь заметно лучше выровнены вокруг
  единых proof surfaces
- RU-стек теперь явно включает Yandex Direct вместе с Webmaster и Metrica

## Как это трактовать в production

- `production_guided` означает, что в репозитории есть контракт, workflow
  shape, verification path и operator routing
- это не означает, что авторы ведут за вас hosted managed service
- целевая модель здесь: self-hosted ownership с явными credentials и review

## Лучший порядок действий

1. подключить одну search или analytics интеграцию
2. проверить environment readiness
3. сделать один manual import
4. просмотреть импортированный baseline
5. перевести это в scheduled checks или CI gating
6. сравнивать дельты после исправлений
