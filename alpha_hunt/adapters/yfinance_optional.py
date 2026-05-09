from __future__ import annotations


def load_bars(*args, **kwargs):
    try:
        import yfinance as yf  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError("Install optional extra first: pip install -e '.[yfinance]'") from exc
    return yf.download(*args, **kwargs)
