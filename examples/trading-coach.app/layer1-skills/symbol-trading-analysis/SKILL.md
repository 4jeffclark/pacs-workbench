---
name: symbol-trading-analysis
description: TradingCoach skill: symbol-trading-analysis
sourceCorpus:
  repository: trading-coach
  path: capabilities/symbol-trading-analysis/
  readOnly: true
metadata:
  legacyCapabilityKind: analyze
---

### Ingest orders

Load order data for `targetSymbol`. Reconstruct entries, adds, reductions, exits, average cost, exposure evolution, realized/unrealized P&L, position timeline, max exposure, turnover. FIFO unless specified.

### Market context

Research symbol and lifecycle period: catalyst, structure, volatility, sector/market context. Factual only for core output.

### Quantitative analysis

Net P&L, max exposure, hold time, average entry/exit, return on max exposure, return on turnover. Defer setup/entry/exit quality judgments to evaluation overlay.

## Used by

- `layer3-playbooks/unit-decision-review`
- `layer3-playbooks/activity-period-review` (multi-symbol variant via `trading-activity-analysis`)