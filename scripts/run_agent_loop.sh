#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${AGENT_CMD:-}" ]]; then
  echo "Set AGENT_CMD to your agent CLI command, e.g. AGENT_CMD='codex'" >&2
  exit 2
fi

$AGENT_CMD "$(cat docs/agent_prompt.md)"
