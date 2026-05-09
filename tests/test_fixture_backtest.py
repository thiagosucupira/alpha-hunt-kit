from pathlib import Path

from alpha_hunt.backtest import run_backtest
from alpha_hunt.schemas import load_json, read_bars_csv

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_backtest_is_deterministic():
    bars = read_bars_csv(ROOT / "fixtures/bars/demo_ohlcv.csv")
    cfg = load_json(ROOT / "experiments/baseline.json")
    first = run_backtest(bars, cfg)
    second = run_backtest(bars, cfg)
    assert first == second
    assert first["bars"] == 160
    assert first["trade_count"] > 0
    assert "score" in first
