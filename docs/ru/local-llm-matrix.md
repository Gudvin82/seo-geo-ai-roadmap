# Матрица Local LLM

Эта матрица нужна как практический starter для команд, которые хотят
self-hosted или privacy-first AI-слой для платформы.

## Top 20 local-ready моделей

| Модель | Роль | Сильная сторона | Комментарий |
|---|---|---|---|
| Llama 3.1 8B | общий audit assistant | баланс цена/качество | хороший старт для небольших серверов |
| Llama 3.1 70B | premium reasoning | лучше длинная аналитика | нужен серьезный GPU-бюджет |
| Llama 3.3 70B | premium reasoning | более свежая instruction-tuning | полезна для drafting отчетов |
| Qwen 2.5 7B | компактный bilingual слой | гибкость EN/RU | хорош для utility-flow |
| Qwen 2.5 14B | content и audit support | сильное multilingual качество | хороший mid-tier default |
| Qwen 2.5 32B | более глубокий анализ | лучше synthesis | выше infra-требования |
| Qwen 2.5 72B | флагманский local reasoning | широкая capability | premium self-hosted tier |
| Mistral 7B | легкий helper | высокая скорость | хорош для triage-задач |
| Mixtral 8x7B | MoE-анализ | сильный structured output | надежен для audit plans |
| Mixtral 8x22B | premium MoE | глубже анализ | дороже в эксплуатации |
| DeepSeek R1 Distill 8B | reasoning | эффективный chain-style подход | хороший benchmark-кандидат |
| DeepSeek R1 Distill 32B | reasoning | сильнее problem solving | полезен для premium lane |
| Phi-4 | компактный assistant | эффективен на слабом железе | хороший внутренний helper |
| Gemma 2 9B | utility generation | чистое следование инструкции | практична для draft-слоя |
| Gemma 2 27B | более богатый output | лучше длинные ответы | умеренные GPU-требования |
| Command R | retrieval-heavy операции | operator-guidance | проверьте licensing |
| Command R+ | premium retrieval | long-context workflows | полезен для document QA |
| Yi 34B | long-form drafting | сильный context handling | зависит от поддержки runtime |
| Nous Hermes 2 | instruction roleplay | operator prompt workflows | хороший fallback |
| Solar 10.7B | компактный reasoning | качественный multilingual drafting | уверенный midweight вариант |

## Рекомендуемые deployment lanes

- Demo или маленькая VPS-лаборатория: `llama3.1:8b`, `qwen2.5:7b`, `mistral:7b`
- Agency default lane: `qwen2.5:14b`, `mixtral`, `gemma2:27b`
- Premium local lane: `llama3.1:70b`, `qwen2.5:72b`, `deepseek-r1-distill:32b`

## Что benchmark-ить

- factual consistency относительно brand facts
- качество EN и RU output
- стабильность structured report formatting
- response time под одновременной нагрузкой операторов
- cost per audit или per report batch

См. также [provider-benchmarks.md](./provider-benchmarks.md) и
[provider-matrix.md](./provider-matrix.md).
