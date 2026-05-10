import os
import json
import shutil
import subprocess
import sys
from pathlib import Path

from alpha_hunt import cli

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


def test_cli_null_gate_failure_discards(tmp_path, monkeypatch, capsys):
    shutil.copytree(ROOT / "experiments", tmp_path / "experiments")
    shutil.copytree(ROOT / "fixtures", tmp_path / "fixtures")
    monkeypatch.chdir(tmp_path)

    def fake_backtest(_bars, _config):
        return {
            "strategy": "current",
            "trade_count": 8,
            "win_rate": 0.5,
            "total_return": 0.01,
            "max_drawdown": -0.01,
            "sharpe_like": 0.2,
            "score": 0.1,
            "null_model": "timestamp_shuffle_same_positions",
            "null_trials": 100,
            "null_score_p95": 0.2,
            "beats_null_p95": False,
        }

    monkeypatch.setattr(cli, "run_backtest", fake_backtest)
    run_id = cli._run(
        Path("experiments/current.json"),
        Path("fixtures/bars/demo_ohlcv.csv"),
        "trial",
        30,
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["decision"] == "DISCARD_CANDIDATE"
    assert payload["metrics"]["beats_null_p95"] is False
    assert "DISCARD_CANDIDATE" in (tmp_path / ".alpha-hunt" / "runs" / run_id / "report.md").read_text()
