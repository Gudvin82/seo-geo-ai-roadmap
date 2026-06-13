# ai.txt Guidance

`ai.txt` is an optional AI-facing guidance file. In this repository it is
treated as a short route map for public AI consumption, not as a replacement
for public facts, `robots.txt`, or `llms.txt`.

## What it is for

- short AI-facing policy hints
- public route guidance
- explicit references to `llms.txt` and sitemap surfaces
- lightweight reminders about what not to invent

## What it is not for

- secret instructions
- legal disclaimers masquerading as crawler policy
- pages or facts that are not visible publicly
- contradictory access rules relative to `robots.txt`

## Minimal pattern

Use [templates/ai.txt.example](../../templates/ai.txt.example) as the baseline.

Recommended directives:

- `policy`
- `summary`
- `contact`
- `llms`
- `sitemap`
- `allow`
- `disallow`
- `notes`

## Validation workflow

1. Draft `ai.txt`.
2. Check that it does not contradict `robots.txt`.
3. Check that it does not drift away from `llms.txt`.
4. Run:

```bash
python scripts/check-ai-txt.py --url https://example.com
```

or

```bash
python scripts/check-ai-txt.py --file ./ai.txt --robots-file ./robots.txt --llms-file ./llms.txt
```

## Common contradictions

- `ai.txt` says broad AI access is welcome while `robots.txt` blocks AI bots
- `ai.txt` mentions `llms.txt` routes that do not exist anymore
- `ai.txt` claims support, pricing, or product facts that the site does not publish

## Honest limitation

`ai.txt` is still an emergent pattern. It may help operator clarity and future
AI hygiene, but it does not create guaranteed crawl or citation behavior.
