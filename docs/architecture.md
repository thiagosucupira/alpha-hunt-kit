# Architecture

```text
idea sources -> hypothesis -> experiment config -> local backtest -> metrics/report
                       ^                                |
                       |                                v
       graveyard <- ledger/current/leaderboard <- promote/bury
```

The package owns the contract. A host runtime only schedules it.

Host examples: shell, cron, GitHub Actions, a coding agent, or a larger private system.
