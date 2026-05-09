#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${PYTHON:-python3}"
rm -rf .alpha-hunt
rm -f state/experiments.tsv state/leaderboard.tsv state/graveyard.jsonl state/sources.jsonl state/current.json
"$PYTHON_BIN" -m alpha_hunt.cli init --demo
