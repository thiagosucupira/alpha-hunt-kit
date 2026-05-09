from pathlib import Path
import json

from alpha_hunt.state import ensure_state

ROOT = Path(__file__).resolve().parents[1]


def test_state_templates_exist():
    ensure_state(ROOT)
    for rel in ["state/current.json", "state/experiments.tsv", "state/leaderboard.tsv", "state/graveyard.jsonl", "state/sources.jsonl"]:
        assert (ROOT / rel).exists()
    current = json.loads((ROOT / "state/current.json").read_text())
    assert "warning" in current
