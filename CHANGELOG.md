# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/ysskrishna/pypi-package-stats-action/releases/tag/v1.0.0
