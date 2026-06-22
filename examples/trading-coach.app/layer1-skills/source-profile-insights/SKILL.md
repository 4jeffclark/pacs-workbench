---
name: source-profile-insights
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: source-profile-insights
metadata:
  legacyCapabilityKind: synthesize
  sourcePath: capabilities/source-profile-insights
  sourceRepository: trading-coach
---

1. Optional developer/trader reflection on coverage gaps and export practices (not trading coaching)
2. Document most useful insights the datastore supports
3. Scorecard on coverage, quality, and treatment readiness
4. Exit interview when evaluation overlay active

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --evaluation false
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Used by

- `layer3-playbooks/source-profile`