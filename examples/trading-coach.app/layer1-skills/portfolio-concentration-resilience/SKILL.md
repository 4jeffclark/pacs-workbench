---
name: portfolio-concentration-resilience
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: portfolio-concentration-resilience
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/portfolio-concentration-resilience
  sourceRepository: trading-coach
---

1. Thesis or category concentration (HHI)
2. Liquidity sleeve analysis
3. Macro overlap and scenario map
4. Report Section 11 (thematic) or 10 (non-thematic)

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE"
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Used by

- `layer3-playbooks/aggregate-state-review`