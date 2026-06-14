# Сводка релиза v4.5.2

`v4.5.2` это упаковочный и продуктовый patch-релиз поверх `v4.5.0`.

## Что изменилось

- Добавлены еще 10 hosted или online providers:
  Hugging Face, Novita, Nebius, Zhipu, Moonshot, DashScope, Qianfan,
  Friendli, Inference.net и универсальный OpenAI-compatible gateway
- Добавлены еще 10 local или self-hosted runtimes:
  LiteLLM, Llamafile, GPT4All, AnythingLLM, Xinference, LlamaSwap, Exo,
  FastChat, H2O.ai h2oGPT и MLX-LM
- `yandex_direct` добавлен как first-class production-guided integration
- Добавлен service-foundation API слой для команд, которые строят свой branded
  scanner или audit service на базе репозитория
- Активные версии приложения и контрактов обновлены до `v4.5.2`

## Почему это важно

- История с провайдерами стала заметно ближе к принципу
  "подключи тот AI, который у тебя уже есть"
- Для RU-рынка стал понятнее Yandex-стек:
  Webmaster, Metrica и Direct
- Репозиторий стал сильнее именно как product foundation, а не только как
  слой методологии
- AI agents получили machine-readable путь для service-builder решений

## Как это интерпретировать

Этот patch не заявляет, что репозиторий уже является SaaS, который
поддерживает автор. Но он честно заявляет следующее:

- платформу можно self-hosted развернуть
- к ней можно подключить более широкий набор провайдеров
- у нее есть реальная scanner и reporting foundation
- ее можно превратить в свой branded service с явной service-builder логикой
  для deployment, планирования SSO, планирования billing и public intake

## Рекомендуемая следующая последовательность

1. Выберите одного hosted провайдера и один local fallback
2. Сначала подключите GSC или Yandex Webmaster
3. Затем добавьте GA4, Metrica или Yandex Direct как outcome layer
4. Используйте service-builder mode, если цель это branded scanner для клиентов
