# Copy-paste agent prompt

You are running the Alpha Hunt loop in this repository.

Goal:
Run one disciplined candidate test on the offline fixture. Improvement only matters if the candidate also passes the enabled falsification gates.

First read:
- README.md
- AGENTS.md
- docs/research_protocol.md
- docs/state_schema.md
- state/current.json
- state/experiments.tsv
- state/graveyard.jsonl

Rules:
1. Run only cheap local experiments unless the user explicitly allows external data.
2. Do not add private dependencies, broker SDKs, secrets, machine-specific paths, or live-trading actions.
3. Prefer editing only:
   - experiments/current.json
   - alpha_hunt/strategies/current.py
4. Every experiment needs a hypothesis. No blind grid search.
5. Before testing, check the graveyard to avoid repeating refuted ideas.
6. Run:
   - `pytest -q`
   - `alpha-hunt trial experiments/current.json --data fixtures/bars/demo_ohlcv.csv --budget-seconds 30`
7. Treat `beats_null_p95=false` as a failed first-pass gate, even if the raw score improved.
8. If the run improves the champion and passes enabled gates, run:
   - `alpha-hunt promote <run_id>`
9. If it fails, run:
   - `alpha-hunt bury <run_id> --reason "<short reason>"`
   Then revert unnecessary code/config changes.
10. Keep notes concise and machine-readable.
11. Repeat until stopped or until you have completed the requested number of experiments.

Start now:
- inspect current state,
- propose one hypothesis,
- make one minimal change,
- run the trial,
- promote or bury it,
- summarize artifact paths and why the result could be wrong.
