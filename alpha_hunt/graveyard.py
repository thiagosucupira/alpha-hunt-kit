from __future__ import annotations

from pathlib import Path
import time

from alpha_hunt.paths import state_dir
from alpha_hunt.state import append_jsonl, ensure_state


def bury(root: Path, run_id: str, reason: str, hypothesis: str = "") -> None:
    ensure_state(root)
    append_jsonl(
        state_dir(root) / "graveyard.jsonl",
        {
            "timestamp": int(time.time()),
            "run_id": run_id,
            "reason": reason,
            "hypothesis": hypothesis,
            "do_not_resurrect_as": reason[:180],
        },
    )
