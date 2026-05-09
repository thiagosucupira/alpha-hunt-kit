from __future__ import annotations

from pathlib import Path
import csv
import json
from typing import Any

from alpha_hunt.paths import state_dir
from alpha_hunt.schemas import write_json

STATE_FILES = {
    "experiments.tsv": "timestamp\trun_id\tstrategy\tscore\tdecision\thypothesis\n",
    "leaderboard.tsv": "timestamp\trun_id\tstrategy\tscore\tnote\n",
    "graveyard.jsonl": "",
    "sources.jsonl": "",
}


def ensure_state(root: Path) -> None:
    sd = state_dir(root)
    sd.mkdir(parents=True, exist_ok=True)
    for name, default in STATE_FILES.items():
        path = sd / name
        if not path.exists():
            path.write_text(default, encoding="utf-8")
    current = sd / "current.json"
    if not current.exists():
        write_json(
            current,
            {
                "champion_run_id": None,
                "strategy": "baseline",
                "score": None,
                "source": "demo-init",
                "warning": "Fixture results prove plumbing only, not edge.",
            },
        )


def read_current(root: Path) -> dict[str, Any]:
    ensure_state(root)
    return json.loads((state_dir(root) / "current.json").read_text(encoding="utf-8"))


def append_tsv(path: Path, row: dict[str, Any], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        if not exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")
