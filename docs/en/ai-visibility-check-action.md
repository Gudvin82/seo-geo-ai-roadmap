# AI Visibility Check GitHub Action

Use the example workflow at
[`examples/github-actions/ai-visibility-check.yml`](../../examples/github-actions/ai-visibility-check.yml)
to run a lightweight GEO/AI check in another repository.

## What it checks

- `llms.txt` structure
- `robots.txt` access for major AI bots
- baseline JSON-LD file validity

## How to adopt it

1. Copy the workflow into `.github/workflows/ai-visibility-check.yml`.
2. Replace the demo URL `https://example.com` with the real site URL.
3. Replace `./llms.txt` if your file lives elsewhere.
4. Replace the schema file path with one of your real JSON-LD files.
5. Run the workflow manually before making it part of PR policy.

## Expected outputs

- pass or fail status for `llms.txt`
- pass or fail status for robots access checks
- pass or fail status for one JSON-LD validation step

## Local dry-run

```bash
python scripts/check-llms-txt.py --file templates/llms.txt.example
python scripts/check-robots-ai-bots.py --url https://example.com
python scripts/schema-validator.py --file templates/schema/organization-schema.json
```

## Failure modes

- `llms.txt` missing or under-specified
- robots rules block important crawlers unintentionally
- schema JSON is invalid or still contains placeholder data

## What it does not prove

- rankings
- guaranteed AI citations
- business lift
