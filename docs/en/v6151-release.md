# v6.15.1 Release Summary

`v6.15.1` is a reliability patch for the v6.15.0 DataForSEO and project-scoped
MCP release. It adds no new integration capabilities and makes no database or
integration-contract changes.

## Fixes

- Corrected the package-relative import for the shared application version so
  repository-level script tests can import the discoverability checker in CI.
- Updated API smoke tests to expect paid DataForSEO syncs to fail closed when
  credentials or explicit operator approval are missing.
- Removed smoke-test assumptions that absent keyword and competitor provider
  data should be fabricated as positive metrics.
- Retained the v6.15.0 DataForSEO consent, budget-guard, cache, and MCP behavior.

## Verification

The release candidate must pass the root and backend pytest suites, Ruff checks,
release hygiene, documentation build, and all required GitHub Actions before the
tag is considered published successfully.
