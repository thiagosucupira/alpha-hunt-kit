from alpha_hunt.graveyard import bury


def test_bury_appends_graveyard_row(tmp_path):
    path = tmp_path / "state/graveyard.jsonl"
    before = path.read_text().count("\n") if path.exists() else 0
    bury(tmp_path, "test-run", "unit-test reason", "unit-test hypothesis")
    after = path.read_text().count("\n")
    assert after == before + 1
    assert "unit-test reason" in path.read_text()
