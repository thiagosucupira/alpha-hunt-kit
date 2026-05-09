import json

from alpha_hunt.state import ensure_state


def test_state_templates_exist(tmp_path):
    ensure_state(tmp_path)
    for rel in ["state/current.json", "state/experiments.tsv", "state/leaderboard.tsv", "state/graveyard.jsonl", "state/sources.jsonl"]:
        assert (tmp_path / rel).exists()
    current = json.loads((tmp_path / "state/current.json").read_text())
    assert "warning" in current
