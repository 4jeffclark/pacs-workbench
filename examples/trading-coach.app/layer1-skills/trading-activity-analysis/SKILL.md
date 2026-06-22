---
name: trading-activity-analysis
description: TradingCoach skill: trading-activity-analysis
sourceCorpus:
  repository: trading-coach
  path: capabilities/trading-activity-analysis/
  readOnly: true
metadata:
  legacyCapabilityKind: analyze
---

### Step 1 — Ingest orders

Load and validate order data. Identify traded symbols, fills, cancels, session dates, long/short when determinable. Reconstruct executions, position lifecycle by symbol, P&L, exposure, turnover, best/worst day/symbol. Use FIFO unless specified; reconcile with gains/losses export when supplied.

### Step 2 — Market context

Research the confirmed period factually (indices, sectors, news, volatility regime). When core-only output, no execution quality judgments.

### Step 3 — Quantitative analysis

Calculate when possible: net P&L, win rate, profit factor, drawdown, max exposure, hold time, symbol-level P&L, daily P&L table (multi-day), concentration metrics. Defer quality judgments to evaluation overlay.

## Outputs

- `Metrics.csv`, daily/symbol rollups
- Report quantification sections

## Used by

- `layer3-playbooks/activity-period-review`