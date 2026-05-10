from __future__ import annotations

from importlib import import_module
import random
from typing import Any

from alpha_hunt.metrics import max_drawdown, sharpe_like, score
from alpha_hunt.schemas import Bar


def _simulate_positions(
    bars: list[Bar], positions: list[int], cost_bps: float
) -> tuple[list[float], list[float], int, int]:
    equity = [1.0]
    returns: list[float] = []
    trades = 0
    wins = 0
    prev_position = 0

    for offset, position in enumerate(positions, start=1):
        changed_position = position != prev_position
        if changed_position:
            trades += 1

        if position == 0:
            r = 0.0
        else:
            r = position * ((bars[offset + 1].close / bars[offset].close) - 1.0)

        if changed_position:
            r -= cost_bps / 10000.0
            prev_position = position

        returns.append(r)
        wins += int(r > 0)
        equity.append(equity[-1] * (1.0 + r))

    return returns, equity, trades, wins


def _summarize(
    strategy_name: str,
    params: dict[str, Any],
    bars_count: int,
    returns: list[float],
    equity: list[float],
    trades: int,
    wins: int,
) -> dict[str, Any]:
    total_return = equity[-1] - 1.0
    max_dd = max_drawdown(equity)
    sharpe = sharpe_like(returns)
    win_rate = wins / len(returns) if returns else 0.0
    return {
        "strategy": strategy_name,
        "params": params,
        "bars": bars_count,
        "trade_count": trades,
        "win_rate": round(win_rate, 6),
        "total_return": round(total_return, 6),
        "max_drawdown": round(max_dd, 6),
        "sharpe_like": round(sharpe, 6),
        "score": score(total_return, sharpe, max_dd, trades),
    }


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round(0.95 * (len(ordered) - 1)))
    return ordered[index]


def run_backtest(bars: list[Bar], config: dict[str, Any]) -> dict[str, Any]:
    strategy_name = config.get("strategy", "current")
    params = dict(config.get("params", {}))
    cost_bps = float(config.get("cost_bps", 0.0))
    module = import_module(f"alpha_hunt.strategies.{strategy_name}")

    positions = [int(module.signal(bars, i, **params)) for i in range(1, len(bars) - 1)]
    returns, equity, trades, wins = _simulate_positions(bars, positions, cost_bps)
    metrics = _summarize(strategy_name, params, len(bars), returns, equity, trades, wins)

    # Cheap candidate-null gate: keep the same position inventory, randomize its timestamps,
    # and ask whether the real timing beats the 95th percentile of shuffled timing.
    # This is a smoke-tier falsification gate, not proof of tradable edge.
    null_trials = int(config.get("null_trials", 0) or 0)
    if null_trials > 0 and positions:
        rng = random.Random(int(config.get("null_seed", 1337)))
        null_scores: list[float] = []
        for _ in range(null_trials):
            shuffled = positions[:]
            rng.shuffle(shuffled)
            n_returns, n_equity, n_trades, _n_wins = _simulate_positions(bars, shuffled, cost_bps)
            n_total_return = n_equity[-1] - 1.0
            n_max_dd = max_drawdown(n_equity)
            n_sharpe = sharpe_like(n_returns)
            null_scores.append(score(n_total_return, n_sharpe, n_max_dd, n_trades))

        null_score_p95 = round(_p95(null_scores), 6)
        metrics.update(
            {
                "null_model": "timestamp_shuffle_same_positions",
                "null_trials": null_trials,
                "null_score_p95": null_score_p95,
                "beats_null_p95": metrics["score"] > null_score_p95,
            }
        )

    return metrics
