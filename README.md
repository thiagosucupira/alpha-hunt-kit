# Alpha Hunt Kit

A small offline harness for falsifying trading ideas with coding agents.

It does not trade. It does not need broker credentials. It does not claim a fixture backtest is alpha. It turns one candidate idea into one bounded experiment, one metrics file, and one keep-or-kill decision.

## Quick start

```bash
git clone https://github.com/thiagosucupira/alpha-hunt-kit.git
cd alpha-hunt-kit
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"

alpha-hunt init --demo
alpha-hunt trial experiments/current.json --data fixtures/bars/demo_ohlcv.csv --budget-seconds 30
alpha-hunt status
pytest -q
```

Expected result:

- `.alpha-hunt/runs/<run_id>/metrics.json`
- `.alpha-hunt/runs/<run_id>/report.md`
- an appended row in `state/experiments.tsv`
- `KEEP_CANDIDATE` or `DISCARD_CANDIDATE`

The committed fixture proves the harness runs. It does not prove a tradable edge.

## The unit of work

A candidate must have:

1. a source or observation,
2. a hypothesis written before the run,
3. a fixed experiment config,
4. explicit cost assumptions,
5. a bounded local backtest,
6. a cheap candidate-null check,
7. a keep/kill decision written to state.

The built-in null check shuffles the candidate's own position sequence across timestamps and asks whether the real timing beats the shuffled 95th percentile. That is a first-pass falsification gate, not final validation.

## Run with an agent

The repo includes agent instructions in `docs/agent_prompt.md` and repository rules in `AGENTS.md`.

```bash
cat docs/agent_prompt.md
```

Or call your agent CLI through the wrapper:

```bash
AGENT_CMD="<your-agent-cli>" scripts/run_agent_loop.sh
```

The intended edit surface is small:

- `experiments/current.json`
- `alpha_hunt/strategies/current.py`
- `state/graveyard.jsonl` when an idea dies

No blind grid search. One hypothesis per run.

## Bring real bars before believing anything

The demo CSV is plumbing. For a serious local read, supply your own normalized OHLCV bars:

```bash
alpha-hunt trial experiments/current.json --data path/to/your_bars.csv --budget-seconds 120
```

CSV columns:

```text
timestamp,open,high,low,close,volume
```

Before trusting a result, document timezone, spread/cost assumption, missing-bar policy, symbol convention, and whether the signal uses only information available at the decision timestamp.

## State files

- `state/current.json`: current champion context.
- `state/experiments.tsv`: append-only trial ledger.
- `state/graveyard.jsonl`: failed ideas and why they died.
- `state/sources.jsonl`: imported paper/idea seeds.
- `experiments/current.json`: editable candidate config.
- `alpha_hunt/strategies/current.py`: editable strategy stub.

## Safety boundary

- Offline by default.
- No network required for tests.
- No broker SDK required.
- No secrets, account IDs, or machine-specific paths.
- Fixture or smoke data can only prove plumbing.
- Failed ideas go to the graveyard instead of being rediscovered.

## License

MIT.
