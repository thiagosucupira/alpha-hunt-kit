from __future__ import annotations

from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "alpha_hunt").exists():
            return candidate
    return cur


def state_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "state"


def runtime_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / ".alpha-hunt"


def runs_dir(root: Path | None = None) -> Path:
    return runtime_dir(root) / "runs"
