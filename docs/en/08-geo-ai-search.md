# GEO and AI Search

> **Tags:** [AI/GEO] [INT] [RU]
> **Priority:** High
> **Roadmap phase:** Month 0-3

## Why this matters

AI assistants recommend pages and brands that are accessible, structured, quotable, and repeatedly cited across the web.

## When to apply

Apply for any brand that wants visibility in ChatGPT, Perplexity, Gemini, Bing Copilot, Google AI Overviews, and Yandex Neural Search.

## Step-by-step instructions

1. Make key content readable as server-rendered HTML.
2. Publish `llms.txt` and, if useful, `llms-full.txt`.
3. Allow relevant AI bots in `robots.txt`.
4. Add answer-ready FAQs, definitions, comparisons, and brand facts.
5. Monitor which competitors and sources LLMs cite for your prompts.

## AI bot access table

| User-Agent | Typical use | Recommended status |
|---|---|---|
| `GPTBot` | model training / discovery policies vary | allow unless legal policy says otherwise |
| `ChatGPT-User` | user-triggered fetch | allow |
| `PerplexityBot` | answer generation and citations | allow |
| `ClaudeBot` | retrieval and citation support | allow |
| `Google-Extended` | Gemini-related training controls | case by case |
| `YandexBot` | search discovery | allow |

## Example `llms.txt` workflow

1. List the main sections of the site.
2. Add short descriptions and canonical URLs.
3. Link key conversion pages, documentation, glossary, and FAQ.
4. Keep the file human-readable and easy to parse.
5. Revisit after each major architecture update.

## Manual AI Share of Voice

1. Build a prompt set around money queries.
2. Ask each AI surface the same questions monthly.
3. Record brand mentions, citations, and sentiment.
4. Note hallucinations and missing facts.
5. Convert findings into content or entity fixes.

## AI Prompt

```text
Create an llms.txt file for this website. Use the homepage, service pages, FAQ, glossary, and company profile. Output concise descriptions and canonical URLs only.
```

## Checklist

- [ ] `llms.txt` published
- [ ] AI bots reviewed in `robots.txt`
- [ ] FAQ and answer-ready content added
- [ ] AI citation tracking started
- [ ] Hallucination log created

## Related sections

- [05-technical-seo.md](./05-technical-seo.md)
- [14-neural-search-ai.md](./14-neural-search-ai.md)
- [18-analytics.md](./18-analytics.md)
