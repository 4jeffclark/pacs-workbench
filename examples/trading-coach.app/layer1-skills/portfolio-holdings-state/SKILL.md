---
name: portfolio-holdings-state
description: TradingCoach skill: portfolio-holdings-state
sourceCorpus:
  repository: trading-coach
  path: capabilities/portfolio-holdings-state/
  readOnly: true
metadata:
  legacyCapabilityKind: transform
---

1. Load canonical `positions_lot_level.csv`, `balances.csv`, `cash.csv` at confirmed snapshot anchors
2. Coordinate with `period-weight-reconstruction` for boundary state
3. Provide position-level evidence for Appendix B

## Outputs

- Boundary MV totals and position inventory
- Inputs to weight and liquidity capabilities

## Used by

- `layer3-playbooks/aggregate-state-review`