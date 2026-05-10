# Research protocol

Alpha Hunt is not a parameter-search machine. It is a falsification loop for trading ideas.

## Loop

1. Source: read a paper, prior run, graveyard row, or market observation.
2. Hypothesize: write one claim that the next run can disprove.
3. Freeze: set the config before seeing the answer.
4. Test: run one bounded local backtest with explicit costs.
5. Gate: compare against the candidate-null check and any user-supplied validation gates.
6. Decide: keep, block, or kill.
7. Remember: update state so the next run starts smarter.

## Valid hypothesis shape

A hypothesis must include:

- thesis: what should happen,
- source: why this seed deserves oxygen,
- observable: which data field proves or falsifies it,
- leakage block: why future data is not leaking into the decision,
- cost model: what friction is included,
- kill criteria: what result ends the idea,
- cheapest next test: the smallest artifact-producing experiment.

## Built-in null gate

`null_trials` in an experiment config enables a cheap timing null: the backtester keeps the candidate's position inventory, shuffles it across timestamps, and computes the 95th percentile shuffled score.

A candidate that does not beat this shuffled p95 is discarded by default. Passing the null gate means "worth a better test," not "edge discovered."

## Default decisions

- KEEP_CANDIDATE: beats the current champion and passes enabled gates.
- DISCARD_CANDIDATE: fails the champion check, null gate, or stated kill criteria.
- BLOCK: cannot be tested honestly with available data; record it in the graveyard with the missing observable.

The default outcome should be DISCARD. Survival is earned.
