---
name: event-trade-context
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: event-trade-context
metadata:
  legacyCapabilityKind: retrieve
  sourcePath: capabilities/event-trade-context
  sourceRepository: trading-coach
---

1. Document event window, offering terms, market reception, lock-up and liquidity constraints when applicable
2. Reconstruct allocation, entry, and exit orders for the symbol
3. Compare outcome to event-day and post-event market path
4. Evaluation overlay: judgment on sizing, timing, and risk management for the event

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --symbol SYMBOL --period-start YYYYMMDD --period-end YYYYMMDD
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Used by

- `layer3-playbooks/unit-decision-review`