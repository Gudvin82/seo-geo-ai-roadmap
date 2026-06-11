# Release Process

## Versioning rules

- Start from `v1.0.0`
- Follow semantic versioning for future releases
- Do not overwrite existing tags

## Release checklist

1. Confirm repository state and current tags.
2. Decide the next version number.
3. Update docs, prompts, templates, scripts, and examples.
4. Update `CHANGELOG.md`.
5. Run markdown and smoke-test workflows locally where possible.
6. Commit with a release-style message.
7. Create a git tag.
8. Push commit and tag.
9. Create a GitHub Release.
10. Verify README rendering and top-level links.

## Commit / tag / release examples

- Commit: `release: ship v1.0.0 discoverability os foundation`
- Tag: `v1.0.0`
- Release title: `v1.0.0 - Foundation release`
