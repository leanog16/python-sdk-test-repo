# Changelog

## Unreleased

### Added
- `bandwidth.tools` package with local development helpers ([docs](docs/Tools.md)):
  - `CallbackStore` for recording and querying callbacks in SQLite
  - `parse_bxml` for turning BXML into Python dictionaries
  - `MediaCache` for caching downloaded media on disk
  - `convert_to_wav` for preparing audio files for `<PlayAudio>`
  - `evaluate_rule` for matching callbacks against routing rules
  - `send_test_callback` for exercising webhook servers

### Changed
- Docstring and type hint cleanups for `Hangup`, `StopGather` and `PlayAudio`
