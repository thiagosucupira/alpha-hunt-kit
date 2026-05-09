import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cmd(*args):
    return subprocess.run(
        [sys.executable, "-m", "alpha_hunt.cli", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_cli_trial_smoke():
    run_cmd("init", "--demo")
    result = run_cmd(
        "trial",
        "experiments/current.json",
        "--data",
        "fixtures/bars/demo_ohlcv.csv",
        "--budget-seconds",
        "30",
    )
    payload = json.loads(result.stdout)
    assert payload["run_id"].endswith("-trial")
    assert payload["decision"] in {"KEEP_CANDIDATE", "DISCARD_CANDIDATE"}
    assert "score" in payload["metrics"]
