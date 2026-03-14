#!/usr/bin/env python3
"""Entrypoint for pypi-package-stats GitHub Action."""

import json
import os
import sys
import uuid
from pathlib import Path

SUMMARY_TEMPLATE = """\
Successfully fetched stats for '{name}'
  Version: {version}
  Downloads (last day):   {last_day:,}
  Downloads (last week):  {last_week:,}
  Downloads (last month): {last_month:,}"""


def get_input(name, required=False, default=None):
    """Read action input from INPUT_* env var."""
    value = os.environ.get(f"INPUT_{name.upper().replace('-', '_')}", "").strip()
    if not value:
        if required:
            print(f"::error::Required input '{name}' is missing or empty.")
            sys.exit(1)
        return default
    return value


def set_output(name, value):
    """Write output to $GITHUB_OUTPUT."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        print(f"  {name}={value}")
        return
    with open(github_output, "a", encoding="utf-8") as f:
        if "\n" in str(value):
            delimiter = f"ghadelimiter_{uuid.uuid4()}"
            f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
        else:
            f.write(f"{name}={value}\n")


def main():
    # Read inputs from env vars (set by action.yml)
    package_name = get_input("package_name", required=True)
    output_path = get_input("output_path", default="stats.json")

    # Import library (top-level re-exports — verified in __init__.py)
    try:
        from pypipackagestats import (
            get_package_stats,
            PackageNotFoundError,
            APIError,
            PyPIStatsError,
        )
    except ImportError:
        print("::error::Failed to import pypipackagestats. Is the package installed?")
        sys.exit(1)

    # Fetch stats, write output, and set summary
    print(f"Fetching stats for package: {package_name}")
    try:
        stats = get_package_stats(package_name, no_cache=True)
        stats_dict = stats.to_dict()
        stats_json = json.dumps(stats_dict, indent=2)

        # Write JSON file
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(stats_json, encoding="utf-8")
        print(f"Stats written to: {out}")

        # Set outputs
        pkg = stats_dict["package"]
        downloads = stats_dict["downloads"]
        set_output("stats-json", stats_json)
        set_output("name", pkg["name"])
        set_output("version", pkg["version"])
        set_output("last-day-downloads", downloads["last_day"])
        set_output("last-week-downloads", downloads["last_week"])
        set_output("last-month-downloads", downloads["last_month"])

        # Summary
        print(SUMMARY_TEMPLATE.format(
            name=package_name,
            version=pkg["version"],
            last_day=downloads["last_day"],
            last_week=downloads["last_week"],
            last_month=downloads["last_month"],
        ))
    except PackageNotFoundError:
        print(f"::error::Package '{package_name}' not found on PyPI.")
        sys.exit(1)
    except APIError as e:
        print(f"::error::API error for '{package_name}': {e}")
        sys.exit(1)
    except PyPIStatsError as e:
        print(f"::error::Error fetching stats for '{package_name}': {e}")
        sys.exit(1)
    except OSError as e:
        print(f"::error::Failed to write to '{output_path}': {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"::error::Unexpected stats response structure: missing key {e}")
        sys.exit(1)
    except Exception as e:
        print(f"::error::Unhandled error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
