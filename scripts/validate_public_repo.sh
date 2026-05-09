#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" scripts/validate_public_repo.py
"$PYTHON_BIN" -m alpha_hunt.cli init --demo
"$PYTHON_BIN" -m alpha_hunt.cli run experiments/baseline.json --data fixtures/bars/demo_ohlcv.csv >/tmp/alpha-hunt-baseline.json
"$PYTHON_BIN" -m alpha_hunt.cli trial experiments/current.json --data fixtures/bars/demo_ohlcv.csv --budget-seconds 30 >/tmp/alpha-hunt-trial.json
"$PYTHON_BIN" -m alpha_hunt.cli status
