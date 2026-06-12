# llms.txt Validator

## What it is

`v3.2.0` includes a free `llms.txt` validator that operators can use in three
aligned ways:

- API endpoint: `POST /api/v1/tools/llms-validator`
- standalone page: [`app/frontend/llms-validator.html`](../../app/frontend/llms-validator.html)
- CLI script: `python scripts/check-llms-txt.py --file ./llms.txt`

The goal is not to certify that a file will "win AI citations". The goal is to
catch obvious structural gaps before the file is shipped to production.

## Current validation rules

The validator currently expects a practical baseline:

- a top-level heading such as `# Example llms.txt`
- structured entries, normally bullet-like lines
- at least one absolute URL such as `https://example.com/faq`
- enough coverage to avoid a nearly empty file
- common trust hints such as homepage, FAQ, and about/trust material

Passing the validator means "good minimum structure". It does not mean the file
is complete for every business or market.

## Passing example

```text
# Example llms.txt
- Home: https://example.com/
- FAQ: https://example.com/faq
- About: https://example.com/about
- Services: https://example.com/services/seo-geo-audit
```

## Typical failure modes

- no heading
- plain text paragraph with no structured entries
- relative paths instead of absolute URLs
- no FAQ/about/trust references
- file too short to be decision-useful

## How to use it

### API

```json
{
  "content": "# Example llms.txt\n- Home: https://example.com/\n- FAQ: https://example.com/faq\n- About: https://example.com/about\n"
}
```

The response returns:

- `is_valid`
- `warnings`
- `recommendations`
- `observed_facts`
- `line_count`
- `checked_source`

### UI

Use the standalone page when you want a fast human-readable check. It is useful
for operators, QA, and client walkthroughs because it explains what failed and
what to fix next.

### CLI

Run local checks before committing:

```bash
python scripts/check-llms-txt.py --file examples/sample-llms.txt
python scripts/check-llms-txt.py --file templates/llms.txt.example
```

## Validation workflow

1. Draft `llms.txt`.
2. Run the validator locally.
3. Fix all structural warnings.
4. Re-check the live hosted file by public URL.
5. Store the passing result in your delivery notes or QA log.

## What to do when it fails

- If the file is too short: add homepage, FAQ, about, contact, and trust pages.
- If URLs are missing: replace relative paths with canonical absolute URLs.
- If structure is missing: convert prose into bullet-like entries.
- If trust hints are missing: add about, proof, policy, or expert pages.

## Alignment rules

The following assets should agree with each other:

- `scripts/check-llms-txt.py`
- `app/backend/app/services/llms_validator.py`
- `app/frontend/llms-validator.html`
- `examples/sample-llms.txt`
- `templates/llms.txt.example`

If one of them accepts a pattern that another rejects, treat it as a release
bug and normalize the rule set.

## Limitations

- the validator checks structure, not business truthfulness
- it does not fetch and compare linked pages
- it does not prove that an LLM will browse or cite the file
- stricter rules may be added in later releases as the operator model matures
