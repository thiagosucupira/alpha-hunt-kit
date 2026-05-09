from __future__ import annotations

from alpha_hunt.schemas import Bar


def signal(bars: list[Bar], index: int, fast: int = 5, slow: int = 20) -> int:
    """Return 1 long, -1 short, 0 flat using a simple moving-average crossover."""
    if index < slow:
        return 0
    closes = [b.close for b in bars]
    fast_ma = sum(closes[index - fast + 1 : index + 1]) / fast
    slow_ma = sum(closes[index - slow + 1 : index + 1]) / slow
    if fast_ma > slow_ma:
        return 1
    if fast_ma < slow_ma:
        return -1
    return 0
