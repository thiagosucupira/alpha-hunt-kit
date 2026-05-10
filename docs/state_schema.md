# State schema

State is intentionally plain text so humans and agents can inspect it.

## state/current.json

```json
{
  "champion_run_id": "20260509-120000-trial",
  "strategy": "current",
  "score": 0.123,
  "params": {"fast": 6, "slow": 18},
  "hypothesis": "Short text",
  "warning": "Fixture results prove plumbing only, not edge."
}
```

## state/experiments.tsv

Columns:

- timestamp
- run_id
- strategy
- score
- decision
- hypothesis

## state/leaderboard.tsv

Columns:

- timestamp
- run_id
- strategy
- score
- note

## state/graveyard.jsonl

One JSON object per killed idea:

```json
{"timestamp": 0, "run_id": "...", "reason": "...", "hypothesis": "...", "do_not_resurrect_as": "..."}
```

## .alpha-hunt/runs/<run_id>/

Runtime artifacts:

- config.json
- metrics.json
- report.md

These are local by default and ignored by git.

`metrics.json` includes ordinary smoke metrics plus enabled gate outputs:

```json
{
  "strategy": "current",
  "trade_count": 12,
  "win_rate": 0.51,
  "total_return": 0.01,
  "max_drawdown": -0.02,
  "sharpe_like": 0.4,
  "score": 0.08,
  "null_model": "timestamp_shuffle_same_positions",
  "null_trials": 100,
  "null_score_p95": 0.12,
  "beats_null_p95": false
}
```

Treat `beats_null_p95=false` as a first-pass failure. The bundled null is intentionally cheap and does not prove edge when it passes; it only asks whether the candidate's realized timing beats shuffled timestamps for the same position inventory.
