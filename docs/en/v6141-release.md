# v6.14.1 Release Summary

`v6.14.1` finalizes the v6.14 integrity release after a CI-only import issue
was discovered on the first tagged commit.

The capability matrix is intentionally dependency-light: documentation and
release checks can generate it without importing optional HTTP client
dependencies. Live connector code loads only when a real provider sync is
requested.

The product scope remains unchanged from v6.14.0:

- generated evidence-bound capability matrix
- calibration protocol for explainable readiness scores
- canonical EN/RU documentation map and parity check
- archived superseded evaluation and launch wrappers

All release checks must pass on this tag before it is treated as the current
public release.
