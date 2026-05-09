from __future__ import annotations

from pathlib import Path
from typing import Any


def write_report(path: Path, run_id: str, config: dict[str, Any], metrics: dict[str, Any], decision: str) -> None:
    lines = [
        f"# Alpha Hunt Run {run_id}",
        "",
        f"Decision: **{decision}**",
        "",
        "## Hypothesis",
        "",
        config.get("hypothesis", "No hypothesis recorded."),
        "",
        "## Metrics",
        "",
    ]
    for key in ["strategy", "trade_count", "win_rate", "total_return", "max_drawdown", "sharpe_like", "score"]:
        lines.append(f"- {key}: `{metrics.get(key)}`")
    lines.extend(
        [
            "",
            "## Caveat",
            "",
            "Fixture or smoke data proves the loop runs. It does not prove a tradable edge.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
