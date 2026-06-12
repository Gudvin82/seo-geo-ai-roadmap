# AI Bots and robots.txt

| Bot | Typical role | Access control hint |
|---|---|---|
| GPTBot | training-oriented bot | manage in `robots.txt` if policy requires |
| ChatGPT-User | user-triggered fetching | allow public pages you want browsed |
| ClaudeBot | crawling or retrieval depending on deployment | keep intent explicit in robots rules |
| PerplexityBot | retrieval and citation-oriented fetching | ensure key pages are reachable |
| Google-Extended | training-use control layer | manage separately from Googlebot |
| Applebot-Extended | extended Apple AI usage control | document access intent explicitly |

## Practical rule

- `robots.txt` controls crawl access intent
- `llms.txt` helps map priority pages and facts
- `ai.txt` can complement AI-facing guidance

## Example directives

```text
User-agent: GPTBot
Disallow:

User-agent: Google-Extended
Disallow: /
```
