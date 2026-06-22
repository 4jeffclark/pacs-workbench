---
name: portfolio-liquidity-analysis
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: portfolio-liquidity-analysis
metadata:
  legacyCapabilityKind: synthesize
  sourcePath: capabilities/portfolio-liquidity-analysis
  sourceRepository: trading-coach
---

1. Produce `LiquidityBreakdown.csv` with period-start/end per component
2. Detail broker cash and cash-equivalent instruments
3. Treat `dual`-role holdings explicitly in narrative

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

- `LiquidityBreakdown.csv`
- Report Section 4 (Cash And Liquidity Analysis)

## CSV schema

```text
Component,Symbol,Account,PeriodStartMarketValue,PeriodEndMarketValue,PeriodChangeMarketValue,LiquidityRole,InstrumentType
```

## Used by

- `layer3-playbooks/aggregate-state-review`