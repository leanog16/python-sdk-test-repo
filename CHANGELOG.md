# Changelog

## Unreleased

### Added
- `bandwidth.utils` package with hand-written helpers ([docs](docs/Utils.md)):
  - Phone number validation and E.164 normalization
  - Constant time verification of callback Basic auth headers
  - `retry_with_backoff` decorator for retrying transient API failures
  - Media Content-Type detection
- `repr()` support for all BXML verbs

### Fixed
- `len()` and indexing on non-nestable BXML verbs (e.g. `Pause`) no longer raise
  `AttributeError`
- Type hints and docstrings for `Pause`, `Ring`, `SendDtmf`, `Tag` and `CustomParam`
