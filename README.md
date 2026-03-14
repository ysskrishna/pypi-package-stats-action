# PyPI Package Stats Action

[![CI](https://github.com/ysskrishna/pypi-package-stats-action/actions/workflows/test.yml/badge.svg)](https://github.com/ysskrishna/pypi-package-stats-action/actions/workflows/test.yml)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-PyPI%20Package%20Stats-blue?logo=github)](https://github.com/marketplace/actions/pypi-package-stats)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A GitHub Action to fetch PyPI package download statistics and metadata. Powered by [pypi-package-stats](https://github.com/ysskrishna/pypi-package-stats).

## Quick Start

```yaml
- uses: ysskrishna/pypi-package-stats-action@v1
  id: stats
  with:
    package-name: 'requests'

- run: echo "Downloads last month: ${{ steps.stats.outputs.last-month-downloads }}"
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `package-name` | PyPI package name to fetch statistics for | Yes | — |
| `output-path` | File path to write the JSON stats output | No | `stats.json` |

## Outputs

| Output | Description |
|--------|-------------|
| `stats-json` | Full JSON string of package statistics |
| `name` | Package name |
| `version` | Current package version on PyPI |
| `last-day-downloads` | Downloads in the last day |
| `last-week-downloads` | Downloads in the last week |
| `last-month-downloads` | Downloads in the last month |

## JSON Output Schema

The `stats-json` output and the file written to `output-path` contain the following structure:

```json
{
  "package": {
    "name": "requests",
    "version": "2.32.3",
    "upload_time": "2024-05-29",
    "description": "Python HTTP for Humans.",
    "author": "Kenneth Reitz",
    "license": "Apache-2.0",
    "home_page": "https://requests.readthedocs.io",
    "pypi_url": "https://pypi.org/project/requests/"
  },
  "downloads": {
    "last_day": 2500000,
    "last_week": 17500000,
    "last_month": 75000000,
    "last_180d": 450000000
  },
  "python_versions": [
    { "version": "3.12", "downloads": 5000000, "percentage": 35.0 },
    { "version": "3.11", "downloads": 4000000, "percentage": 28.0 }
  ],
  "operating_systems": [
    { "os": "Linux", "downloads": 12000000, "percentage": 68.0 },
    { "os": "Windows", "downloads": 3500000, "percentage": 20.0 },
    { "os": "Darwin", "downloads": 2000000, "percentage": 12.0 }
  ]
}
```

## Usage Examples

### Basic — Print Download Stats

```yaml
name: Package Stats
on: workflow_dispatch

jobs:
  stats:
    runs-on: ubuntu-latest
    steps:
      - uses: ysskrishna/pypi-package-stats-action@v1
        id: stats
        with:
          package-name: 'social-links'

      - name: Print stats
        env:
          PKG_NAME: ${{ steps.stats.outputs.name }}
          PKG_VERSION: ${{ steps.stats.outputs.version }}
          DL_DAY: ${{ steps.stats.outputs.last-day-downloads }}
          DL_WEEK: ${{ steps.stats.outputs.last-week-downloads }}
          DL_MONTH: ${{ steps.stats.outputs.last-month-downloads }}
        run: |
          echo "Package: $PKG_NAME v$PKG_VERSION"
          echo "Downloads (day):   $DL_DAY"
          echo "Downloads (week):  $DL_WEEK"
          echo "Downloads (month): $DL_MONTH"
```

### Save Stats as Artifact

```yaml
- uses: ysskrishna/pypi-package-stats-action@v1
  with:
    package-name: 'nestedutils'
    output-path: 'reports/nestedutils-stats.json'

- uses: actions/upload-artifact@v4
  with:
    name: package-stats
    path: reports/nestedutils-stats.json
```

### Check Download Threshold

```yaml
- uses: ysskrishna/pypi-package-stats-action@v1
  id: stats
  with:
    package-name: 'container-detect'

- name: Check download threshold
  env:
    DL_MONTH: ${{ steps.stats.outputs.last-month-downloads }}
  run: |
    if [ "$DL_MONTH" -lt 1000 ]; then
      echo "::warning::Monthly downloads ($DL_MONTH) are below 1000"
    fi
```

### Custom Output Path

```yaml
- uses: ysskrishna/pypi-package-stats-action@v1
  with:
    package-name: 'video-extensions'
    output-path: 'output/video-extensions-stats.json'

- name: Read stats file
  run: cat output/video-extensions-stats.json | python3 -m json.tool
```

## Error Handling

The action fails with a clear error message when:

- **Package not found** — The specified package does not exist on PyPI
- **API error** — PyPI or pypistats.org API is unreachable or returns an error
- **Write error** — The output file path is not writable

Errors are surfaced in the GitHub Actions UI via `::error::` workflow commands.

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](LICENSE) for details.

## Credits

Built on [pypi-package-stats](https://github.com/ysskrishna/pypi-package-stats) — a Python library for fetching PyPI package statistics.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://github.com/ysskrishna/pypi-package-stats">pypi-package-stats Library</a> •
  <a href="https://github.com/ysskrishna/pypi-package-stats-action/issues">Report Issues</a> •
  <a href="https://github.com/ysskrishna/pypi-package-stats-action/releases">Releases</a>
</p>
