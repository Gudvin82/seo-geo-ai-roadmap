# AI Citation Score

## What it measures

AI Citation Score is a transparent `0-100` signal showing whether a brand is:

- mentioned
- cited
- described with acceptable answer quality

across a defined set of prompts and providers.

## How it is calculated

The current implementation derives the score from structured AI SoV results:

- mention presence
- citation count
- answer quality

The score is intentionally simple and reviewable. It is not a hidden model.

## What it is good for

- tracking whether a brand is visible across repeated AI SoV runs
- comparing deltas after factual and structural fixes
- adding one more measurable layer to discoverability reporting

## Limitations

- AI answer surfaces are volatile
- providers behave differently
- prompt wording changes outcomes
- a higher score does not guarantee business results by itself

Use it as a trend signal, not as a standalone truth claim.
