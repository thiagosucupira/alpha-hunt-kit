from alpha_hunt.adapters.csv_bars import load_bars


def test_csv_adapter_loads_fixture():
    bars = load_bars("fixtures/bars/demo_ohlcv.csv")
    assert len(bars) == 160
    assert bars[0].timestamp.endswith("Z")
