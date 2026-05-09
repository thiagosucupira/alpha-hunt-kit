from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from alpha_hunt.backtest import run_backtest
from alpha_hunt.graveyard import bury as bury_run
from alpha_hunt.paths import repo_root, runs_dir, state_dir
from alpha_hunt.report import write_report
from alpha_hunt.schemas import load_json, read_bars_csv, write_json
from alpha_hunt.sources import ingest as ingest_sources
from alpha_hunt.state import append_tsv, ensure_state, read_current


def _run(config_path: Path, data_path: Path, mode: str, budget_seconds: int | None = None) -> str:
    root = repo_root()
    ensure_state(root)
    start = time.time()
    config = load_json(config_path)
    bars = read_bars_csv(data_path)
    metrics = run_backtest(bars, config)
    if budget_seconds is not None and time.time() - start > budget_seconds:
        raise SystemExit(f"Budget exceeded: {budget_seconds}s")

    run_id = time.strftime("%Y%m%d-%H%M%S") + f"-{mode}"
    out = runs_dir(root) / run_id
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "config.json", config)
    write_json(out / "metrics.json", metrics)

    current = read_current(root)
    champion_score = current.get("score")
    if champion_score is None or metrics["score"] > float(champion_score):
        decision = "KEEP_CANDIDATE"
    else:
        decision = "DISCARD_CANDIDATE"
    write_report(out / "report.md", run_id, config, metrics, decision)

    append_tsv(
        state_dir(root) / "experiments.tsv",
        {
            "timestamp": int(time.time()),
            "run_id": run_id,
            "strategy": metrics["strategy"],
            "score": metrics["score"],
            "decision": decision,
            "hypothesis": config.get("hypothesis", ""),
        },
        ["timestamp", "run_id", "strategy", "score", "decision", "hypothesis"],
    )
    print(json.dumps({"run_id": run_id, "decision": decision, "metrics": metrics}, indent=2, sort_keys=True))
    return run_id


def cmd_init(args: argparse.Namespace) -> None:
    root = repo_root()
    ensure_state(root)
    if args.demo:
        ingest_sources(root, root / "fixtures" / "sources" / "seed_sources.jsonl")
    print(f"Initialized Alpha Hunt state at {state_dir(root)}")


def cmd_run(args: argparse.Namespace) -> None:
    _run(Path(args.config), Path(args.data), "run")


def cmd_trial(args: argparse.Namespace) -> None:
    _run(Path(args.config), Path(args.data), "trial", args.budget_seconds)


def cmd_promote(args: argparse.Namespace) -> None:
    root = repo_root()
    metrics_path = runs_dir(root) / args.run_id / "metrics.json"
    config_path = runs_dir(root) / args.run_id / "config.json"
    if not metrics_path.exists():
        raise SystemExit(f"Run not found: {args.run_id}")
    metrics = load_json(metrics_path)
    config = load_json(config_path)
    write_json(
        state_dir(root) / "current.json",
        {
            "champion_run_id": args.run_id,
            "strategy": metrics["strategy"],
            "score": metrics["score"],
            "params": metrics.get("params", {}),
            "hypothesis": config.get("hypothesis", ""),
            "warning": "Fixture results prove plumbing only, not edge.",
        },
    )
    append_tsv(
        state_dir(root) / "leaderboard.tsv",
        {
            "timestamp": int(time.time()),
            "run_id": args.run_id,
            "strategy": metrics["strategy"],
            "score": metrics["score"],
            "note": args.note,
        },
        ["timestamp", "run_id", "strategy", "score", "note"],
    )
    print(f"Promoted {args.run_id} with score {metrics['score']}")


def cmd_bury(args: argparse.Namespace) -> None:
    root = repo_root()
    config_path = runs_dir(root) / args.run_id / "config.json"
    hypothesis = ""
    if config_path.exists():
        hypothesis = load_json(config_path).get("hypothesis", "")
    bury_run(root, args.run_id, args.reason, hypothesis)
    print(f"Buried {args.run_id}: {args.reason}")


def cmd_sources_ingest(args: argparse.Namespace) -> None:
    root = repo_root()
    count = ingest_sources(root, Path(args.path))
    print(f"Ingested {count} source rows")


def cmd_status(args: argparse.Namespace) -> None:
    root = repo_root()
    ensure_state(root)
    current = read_current(root)
    graveyard = state_dir(root) / "graveyard.jsonl"
    experiments = state_dir(root) / "experiments.tsv"
    runs = sorted(runs_dir(root).glob("*")) if runs_dir(root).exists() else []
    print("Alpha Hunt status")
    print(f"- champion: {current.get('champion_run_id')} score={current.get('score')} strategy={current.get('strategy')}")
    print(f"- runs: {len(runs)}")
    print(f"- experiments log: {experiments}")
    print(f"- graveyard rows: {sum(1 for _ in graveyard.open(encoding='utf-8')) if graveyard.exists() else 0}")
    print("- reminder: fixture data proves plumbing only, not edge")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alpha-hunt")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("init")
    p.add_argument("--demo", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("run")
    p.add_argument("config")
    p.add_argument("--data", required=True)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("trial")
    p.add_argument("config")
    p.add_argument("--data", required=True)
    p.add_argument("--budget-seconds", type=int, default=30)
    p.set_defaults(func=cmd_trial)

    p = sub.add_parser("promote")
    p.add_argument("run_id")
    p.add_argument("--note", default="promoted by operator/agent")
    p.set_defaults(func=cmd_promote)

    p = sub.add_parser("bury")
    p.add_argument("run_id")
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_bury)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("sources")
    source_sub = p.add_subparsers(required=True)
    ingest = source_sub.add_parser("ingest")
    ingest.add_argument("path")
    ingest.set_defaults(func=cmd_sources_ingest)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
