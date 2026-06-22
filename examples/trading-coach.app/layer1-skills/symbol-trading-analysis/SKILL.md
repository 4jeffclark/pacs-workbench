---
name: symbol-trading-analysis
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: symbol-trading-analysis
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/symbol-trading-analysis
  sourceRepository: trading-coach
---

### Ingest orders

Load order data for `targetSymbol`. Reconstruct entries, adds, reductions, exits, average cost, exposure evolution, realized/unrealized P&L, position timeline, max exposure, turnover. FIFO unless specified.

### Market context

Research symbol and lifecycle period: catalyst, structure, volatility, sector/market context. Factual only for core output.

### Quantitative analysis

Net P&L, max exposure, hold time, average entry/exit, return on max exposure, return on turnover. Defer setup/entry/exit quality judgments to evaluation overlay.

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
- `layer3-playbooks/activity-period-review` (multi-symbol variant via `trading-activity-analysis`)