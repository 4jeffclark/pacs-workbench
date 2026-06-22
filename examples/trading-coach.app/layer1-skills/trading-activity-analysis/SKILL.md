---
name: trading-activity-analysis
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: trading-activity-analysis
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/trading-activity-analysis
  sourceRepository: trading-coach
---

### Step 1 — Ingest orders

Load and validate order data. Identify traded symbols, fills, cancels, session dates, long/short when determinable. Reconstruct executions, position lifecycle by symbol, P&L, exposure, turnover, best/worst day/symbol. Use FIFO unless specified; reconcile with gains/losses export when supplied.

### Step 2 — Market context

Research the confirmed period factually (indices, sectors, news, volatility regime). When core-only output, no execution quality judgments.

### Step 3 — Quantitative analysis

Calculate when possible: net P&L, win rate, profit factor, drawdown, max exposure, hold time, symbol-level P&L, daily P&L table (multi-day), concentration metrics. Defer quality judgments to evaluation overlay.

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --period-start YYYYMMDD --period-end YYYYMMDD
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- `Metrics.csv`, daily/symbol rollups
- Report quantification sections

## Used by

- `layer3-playbooks/activity-period-review`