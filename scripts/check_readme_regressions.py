#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys

README_PATH = pathlib.Path("README.md")
README_TEXT = README_PATH.read_text(encoding="utf-8")

CHECKS: list[tuple[str, str]] = [
    (
        "TSS version FAQ note",
        r"TSS version alone does \*\*not\*\* tell you whether a vehicle has TSK/SecOC",
    ),
    (
        "EU vs US RAV4 FAQ note",
        r"EU 2024 RAV4 Hybrid appears to have TSK, while the US 2025 RAV4 appears not to have TSK",
    ),
    (
        "openpilot freshness badge",
        r"img\.shields\.io/github/last-commit/commaai/openpilot/nightly-dev",
    ),
    (
        "sunnypilot release-tizi freshness badge",
        r"img\.shields\.io/github/last-commit/sunnypilot/sunnypilot/release-tizi",
    ),
    (
        "FrogPilot freshness badge",
        r"img\.shields\.io/github/last-commit/FrogAi/FrogPilot/FrogPilot",
    ),
    (
        "SatoPilot personal3 freshness badge",
        r"img\.shields\.io/github/last-commit/AlexandreSato/openpilot/personal3",
    ),
]


def main() -> int:
    failed = False
    for label, pattern in CHECKS:
        if re.search(pattern, README_TEXT, flags=re.MULTILINE) is None:
            failed = True
            print(f"Missing expected README content: {label}", file=sys.stderr)
    if failed:
        return 1
    print("README regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
