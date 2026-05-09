from __future__ import annotations

from importlib import import_module
from typing import Any

from alpha_hunt.metrics import max_drawdown, sharpe_like, score
from alpha_hunt.schemas import Bar


def run_backtest(bars: list[Bar], config: dict[str, Any]) -> dict[str, Any]:
    strategy_name = config.get("strategy", "current")
    params = dict(config.get("params", {}))
    cost_bps = float(config.get("cost_bps", 0.0))
    module = import_module(f"alpha_hunt.strategies.{strategy_name}")

    equity = [1.0]
    returns: list[float] = []
    trades = 0
    wins = 0
    prev_position = 0

    for i in range(1, len(bars) - 1):
        position = int(module.signal(bars, i, **params))
        changed_position = position != prev_position
        if changed_position:
            trades += 1
            prev_position = position
        if position == 0:
            r = 0.0
        else:
            r = position * ((bars[i + 1].close / bars[i].close) - 1.0)
            if changed_position:
                r -= cost_bps / 10000.0
        returns.append(r)
        wins += int(r > 0)
        equity.append(equity[-1] * (1.0 + r))

    total_return = equity[-1] - 1.0
    max_dd = max_drawdown(equity)
    sharpe = sharpe_like(returns)
    win_rate = wins / len(returns) if returns else 0.0
    return {
        "strategy": strategy_name,
        "params": params,
        "bars": len(bars),
        "trade_count": trades,
        "win_rate": round(win_rate, 6),
        "total_return": round(total_return, 6),
        "max_drawdown": round(max_dd, 6),
        "sharpe_like": round(sharpe, 6),
        "score": score(total_return, sharpe, max_dd, trades),
    }
