from __future__ import annotations

from pathlib import Path
from alpha_hunt.schemas import Bar, read_bars_csv


def load_bars(path: str | Path) -> list[Bar]:
    return read_bars_csv(path)
