from __future__ import annotations

from alpha_hunt.schemas import Bar


def signal(bars: list[Bar], index: int, fast: int = 6, slow: int = 18) -> int:
    """Agent-editable strategy. Keep it tiny, auditable, and fixture-safe."""
    if index < slow:
        return 0
    closes = [b.close for b in bars]
    fast_ma = sum(closes[index - fast + 1 : index + 1]) / fast
    slow_ma = sum(closes[index - slow + 1 : index + 1]) / slow
    # Deadband avoids flipping on tiny noise.
    threshold = 0.0005 * bars[index].close
    if fast_ma > slow_ma + threshold:
        return 1
    if fast_ma < slow_ma - threshold:
        return -1
    return 0
