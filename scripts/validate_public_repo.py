#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BANNED_PATTERNS = [
    r"/home/",
    r"/Users/",
    r"\.openclaw",
    r"\.hermes",
    r"broker[_-]?id",
    r"account[_-]?id",
    r"api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}",
    r"secret\s*[:=]\s*['\"][^'\"]{8,}",
]
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".alpha-hunt", "dist", "build"}
TEXT_EXTS = {".py", ".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".sh", ".gitignore", ""}


def iter_files():
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name == "validate_public_repo.py":
            continue
        if path.is_file() and (path.suffix in TEXT_EXTS or path.name in {"LICENSE", "AGENTS.md"}):
            yield path


def main() -> int:
    violations = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in BANNED_PATTERNS:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                violations.append((path.relative_to(ROOT), pat, m.start()))
    if violations:
        print("Public repo validation failed:")
        for path, pat, pos in violations:
            print(f"- {path}: pattern {pat!r} near char {pos}")
        return 1
    print("Public repo validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
