from __future__ import annotations

import math


def max_drawdown(equity: list[float]) -> float:
    peak = equity[0]
    worst = 0.0
    for value in equity:
        peak = max(peak, value)
        dd = (value / peak) - 1.0 if peak else 0.0
        worst = min(worst, dd)
    return worst


def sharpe_like(returns: list[float]) -> float:
    if len(returns) < 2:
        return 0.0
    mean = sum(returns) / len(returns)
    var = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    sd = math.sqrt(var)
    if sd == 0:
        return 0.0
    return mean / sd * math.sqrt(252)


def score(total_return: float, sharpe: float, max_dd: float, trade_count: int) -> float:
    # Penalize shallow/no-trade artifacts. This is a demo score, not a finance claim.
    activity = min(1.0, trade_count / 8.0)
    risk_penalty = abs(max_dd) * 0.8
    return round((total_return * 2.0 + sharpe * 0.25 - risk_penalty) * activity, 6)
