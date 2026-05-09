# Agent rules for Alpha Hunt Kit

You are inside a public, offline-first alpha research project.

Read before editing:
- README.md
- docs/research_protocol.md
- docs/state_schema.md
- docs/agent_prompt.md
- state/current.json
- state/experiments.tsv
- state/graveyard.jsonl

Rules:
1. Run only cheap local experiments unless the user explicitly allows external data.
2. Do not add private dependencies, broker SDKs, secrets, machine-specific paths, or live-trading actions.
3. Prefer editing only `experiments/current.json` and `alpha_hunt/strategies/current.py`.
4. Every experiment needs a hypothesis. No blind grid search.
5. Check the graveyard before testing so you do not repeat refuted ideas.
6. Run `pytest -q` and `alpha-hunt trial experiments/current.json --data fixtures/bars/demo_ohlcv.csv --budget-seconds 30`.
7. If the result improves the champion and passes constraints, run `alpha-hunt promote <run_id>`.
8. If it fails, run `alpha-hunt bury <run_id> --reason "<short reason>"` and revert unnecessary changes.
9. Keep notes concise and artifact-backed.
10. Fixture results prove plumbing, not edge.
