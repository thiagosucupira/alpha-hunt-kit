from pathlib import Path

from alpha_hunt.graveyard import bury

ROOT = Path(__file__).resolve().parents[1]


def test_bury_appends_graveyard_row():
    path = ROOT / "state/graveyard.jsonl"
    before = path.read_text().count("\n") if path.exists() else 0
    bury(ROOT, "test-run", "unit-test reason", "unit-test hypothesis")
    after = path.read_text().count("\n")
    assert after == before + 1
    assert "unit-test reason" in path.read_text()
