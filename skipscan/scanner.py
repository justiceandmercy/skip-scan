"""Core scanning logic for skip-scan."""

from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from typing import Iterable

from .patterns import IGNORED_DIRS, IGNORED_EXTS, patterns_for


@dataclass
class Finding:
    file: str
    line: int
    kind: str
    snippet: str

    def to_dict(self) -> dict:
        return asdict(self)


def _walk(root: str) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored dirs in place
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            full = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            if ext in IGNORED_EXTS:
                continue
            if not patterns_for(full):
                continue
            yield full


def scan(root: str, include: set[str] | None = None) -> list[Finding]:
    """Scan *root* for skipped/focused tests. Returns a list of Finding."""
    findings: list[Finding] = []
    for path in _walk(root):
        if include is not None:
            ext = os.path.splitext(path)[1].lower()
            if ext not in include:
                continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
        except OSError:
            continue
        pats = patterns_for(path)
        rel = os.path.relpath(path, root) if os.path.isabs(root) else path
        for idx, raw in enumerate(lines, start=1):
            line = raw.rstrip("\n")
            if "skip-scan:ignore" in line or "skip-scan: ignore" in line:
                continue
            for kind, rx in pats:
                if rx.search(line):
                    findings.append(
                        Finding(file=rel, line=idx, kind=kind, snippet=line.strip())
                    )
                    break  # one finding per line is enough
    findings.sort(key=lambda f: (f.file, f.line))
    return findings
