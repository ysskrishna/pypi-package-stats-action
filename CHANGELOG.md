# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0]

### Added

- GitHub Job Summary — a Markdown stats table is automatically written to the workflow run's Summary page
- Log tip reminding users to set `id` on the action step and listing alternative ways to access stats (JSON file, Job Summary)
- Output path validation — `output-path` is now verified to stay within `$GITHUB_WORKSPACE`
- "Accessing Stats" section in README documenting the 3 ways to retrieve results (step outputs, JSON file, Job Summary)
- Link to the new [examples repository](https://github.com/ysskrishna/pypi-package-stats-action-examples) in README and footer

### Changed

- Refactored `scripts/run.py` — consolidated stats fetching, file writing, and output setting into a single `try` block with granular exception handling (`PackageNotFoundError`, `APIError`, `OSError`, `KeyError`)
- Download counts are now formatted with comma separators and fall back to `"unknown"` when missing
- README usage examples replaced with a table linking to the examples repository to avoid duplication

## [1.0.0]

### Added

- Initial release of PyPI Package Stats GitHub Action
- Composite action using `pypi-package-stats` Python library
- Inputs:
  - `package-name` (required) — PyPI package name to fetch statistics for
  - `output-path` (optional, default: `stats.json`) — file path for JSON output
- Outputs:
  - `stats-json` — full JSON string of package statistics
  - `name` — package name
  - `version` — current package version on PyPI
  - `last-day-downloads` — downloads in the last day
  - `last-week-downloads` — downloads in the last week
  - `last-month-downloads` — downloads in the last month
- JSON file output with package metadata, download stats, Python version breakdown, and OS distribution
- Error handling with `::error::` workflow commands for GitHub Actions UI
- CI workflow with 3 test jobs (basic usage, custom output path, invalid package)
- Automated GitHub Release creation via `publish.yml` workflow on tag push

[1.1.0]: https://github.com/ysskrishna/pypi-package-stats-action/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ysskrishna/pypi-package-stats-action/releases/tag/v1.0.0
