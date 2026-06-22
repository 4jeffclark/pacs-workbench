# TradingCoach APP Distribution Repo

APP distribution repo root (workbench path: `examples/`). Contains indexed APP instances only.

## Packs

| Pack | Path | Description |
| --- | --- | --- |
| TradingCoach | [trading-coach.app/](trading-coach.app/) | Portfolio analysis and trading performance review playbooks |

## Execution

Point the executor at this repo and pack `APP-EXECUTION.md`:

```yaml
appRepo: <path-to-this-repo>
directive:
  pack: trading-coach
  playbook: aggregate-state-review
inputs:
  userDatastore: ~/TradingCoachData
```

See [trading-coach.app/APP-EXECUTION.md](trading-coach.app/APP-EXECUTION.md).
