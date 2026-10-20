"""Language-specific patterns for skipped / focused tests."""

from __future__ import annotations

import re

# Map file extension -> list of (kind label, compiled regex).
PATTERNS: dict[str, list[tuple[str, re.Pattern]]] = {
    ".py": [
        ("pytest.skip", re.compile(r"\bpytest\.skip\s*\(")),
        ("pytest.mark.skip", re.compile(r"@pytest\.mark\.skip(?:if)?\b")),  # skip-scan:ignore
        ("pytest.mark.xfail", re.compile(r"@pytest\.mark\.xfail\b")),
        ("unittest.skip", re.compile(r"@unittest\.skip(?:If|Unless)?\b")),  # skip-scan:ignore
        ("unittest.expectedFailure", re.compile(r"@unittest\.expectedFailure\b")),
        ("skip call", re.compile(r"\.skip\s*\(")),
    ],
    ".js": [
        ("it.skip", re.compile(r"\b(?:it|test|describe|context)\.skip\s*\(")),
        ("xit/xtest", re.compile(r"\bx(?:it|test|describe)\s*\(")),
        ("fit/fdescribe", re.compile(r"\bf(?:it|describe|context)\s*\(")),
        ("skip call", re.compile(r"\.skip\s*\(")),
    ],
    ".ts": [],
    ".jsx": [],
    ".tsx": [],
    ".go": [
        ("t.Skip", re.compile(r"\bt\.Skip(?:f)?\s*\(")),
        ("skip build tag", re.compile(r"//\s*go:build\s+!")),
    ],
    ".rs": [
        ("#[ignore]", re.compile(r"#\[\s*ignore\s*\]")),
        ("ignored test", re.compile(r"#\[\s*ignore\s*=\s*")),
    ],
    ".java": [
        ("@Disabled", re.compile(r"@Disabled\b")),
        ("@Ignore", re.compile(r"@Ignore\b")),
    ],
    ".rb": [
        ("skip", re.compile(r"\bskip\b\s*['\"]")),
        ("xit/xdescribe", re.compile(r"\bx(?:it|describe|context)\b")),
        ("fit/fdescribe", re.compile(r"\bf(?:it|describe|context)\b")),
    ],
}

# JS-family extensions reuse the .js patterns.
for _ext in (".ts", ".jsx", ".tsx", ".mjs", ".cjs"):
    PATTERNS[_ext] = PATTERNS[".js"]

# Extensions we never treat as source.
IGNORED_DIRS = {
    ".git", "node_modules", "venv", ".venv", "env", ".env", "__pycache__",
    "dist", "build", "target", ".idea", ".vscode", ".tox", "coverage",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
}

IGNORED_EXTS = {
    ".min.js", ".map", ".lock", ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".ico", ".pdf", ".zip", ".tar", ".gz", ".bin", ".pyc",
}


def patterns_for(path: str) -> list[tuple[str, re.Pattern]]:
    import os

    ext = os.path.splitext(path)[1].lower()
    return PATTERNS.get(ext, [])
