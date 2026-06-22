---
name: portfolio-period-flows
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: portfolio-period-flows
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/portfolio-period-flows
  sourceRepository: trading-coach
---

1. Filter filled orders to analysis period
2. Aggregate by symbol and mapped thesis/category
3. Feed `portfolio-evolution` and Appendix B order tables

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --period-start YYYYMMDD --period-end YYYYMMDD
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Used by

- `layer3-playbooks/aggregate-state-review`