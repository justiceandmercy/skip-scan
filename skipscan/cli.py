"""Command-line entry point for skip-scan."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .scanner import scan


def _parse_include(value: str | None) -> set[str] | None:
    if not value:
        return None
    parts = [p.strip().lower() for p in value.split(",") if p.strip()]
    out = set()
    for p in parts:
        if not p.startswith("."):
            p = "." + p
        out.add(p)
    return out or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skip-scan",
        description="Find skipped and focused tests in a repository.",
    )
    parser.add_argument("path", nargs="?", default=".", help="root to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--include", help="comma-separated extensions to scan, e.g. .py,.ts"
    )
    parser.add_argument(
        "--fail", action="store_true", help="exit non-zero if skips are found"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        help="allowed number of skips before --fail triggers (default 0)",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    include = _parse_include(args.include)
    findings = scan(args.path, include=include)

    if args.json:
        print(json.dumps([f.to_dict() for f in findings], indent=2))
    else:
        for f in findings:
            print(f"{f.file}:{f.line}: {f.snippet}")
        if findings:
            print(f"\n{len(findings)} skipped/focused test(s) found.", file=sys.stderr)

    if args.fail and len(findings) > args.threshold:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
