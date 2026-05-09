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
