from __future__ import annotations

from pathlib import Path
import json

from alpha_hunt.paths import state_dir
from alpha_hunt.state import append_jsonl, ensure_state


def ingest(root: Path, source_path: Path) -> int:
    ensure_state(root)
    count = 0
    for line in source_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        append_jsonl(state_dir(root) / "sources.jsonl", payload)
        count += 1
    return count
