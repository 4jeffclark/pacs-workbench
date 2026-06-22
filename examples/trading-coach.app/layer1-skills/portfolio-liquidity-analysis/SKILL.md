---
name: portfolio-liquidity-analysis
description: TradingCoach skill: portfolio-liquidity-analysis
sourceCorpus:
  repository: trading-coach
  path: capabilities/portfolio-liquidity-analysis/
  readOnly: true
metadata:
  legacyCapabilityKind: synthesize
---

1. Produce `LiquidityBreakdown.csv` with period-start/end per component
2. Detail broker cash and cash-equivalent instruments
3. Treat `dual`-role holdings explicitly in narrative

## Outputs

- `LiquidityBreakdown.csv`
- Report Section 4 (Cash And Liquidity Analysis)

## CSV schema

```text
Component,Symbol,Account,PeriodStartMarketValue,PeriodEndMarketValue,PeriodChangeMarketValue,LiquidityRole,InstrumentType
```

## Used by

- `layer3-playbooks/aggregate-state-review`