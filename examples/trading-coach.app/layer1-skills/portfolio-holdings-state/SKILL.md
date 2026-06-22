---
name: portfolio-holdings-state
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: portfolio-holdings-state
metadata:
  legacyCapabilityKind: transform
  sourcePath: capabilities/portfolio-holdings-state
  sourceRepository: trading-coach
---

1. Load canonical `positions_lot_level.csv`, `balances.csv`, `cash.csv` at confirmed snapshot anchors
2. Coordinate with `period-weight-reconstruction` for boundary state
3. Provide position-level evidence for Appendix B

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE"
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- Boundary MV totals and position inventory
- Inputs to weight and liquidity capabilities

## Used by

- `layer3-playbooks/aggregate-state-review`