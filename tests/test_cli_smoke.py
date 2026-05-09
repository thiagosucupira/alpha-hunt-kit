import os
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cmd(cwd: Path, *args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return subprocess.run(
        [sys.executable, "-m", "alpha_hunt.cli", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def test_cli_trial_smoke(tmp_path):
    shutil.copytree(ROOT / "experiments", tmp_path / "experiments")
    shutil.copytree(ROOT / "fixtures", tmp_path / "fixtures")
    run_cmd(tmp_path, "init", "--demo")
    result = run_cmd(
        tmp_path,
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
    assert (tmp_path / "state/experiments.tsv").exists()
