# Data adapters

The offline demo must work with no network and no keys. Optional adapters can be added, but they must fail gracefully.

## Required adapter

- `csv_bars`: reads `timestamp,open,high,low,close,volume` CSV.

## Optional tiers

1. Fixture data: committed demo data. Proves plumbing only.
2. Public smoke/reference feeds: useful for demos, not validation.
3. Public/manual history: useful after normalization and license checks.
4. API-key providers: Alpha Vantage, Twelve Data, Tiingo, Polygon.
5. Broker/account adapters: OANDA, Darwinex, FXCM, IBKR.
6. Host canonical bars: required for serious promoted claims.

## Rule

If an adapter requires a key, account, manual download, or broker terms, it is optional and must not be part of CI.
