---
name: thesis-health
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: thesis-health
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/thesis-health
  sourceRepository: trading-coach
---

**When `thematic: true`:**

1. Per owned thesis: momentum, relative strength, volatility, drawdown, breadth/flow proxies, catalysts
2. `ThesisHealth.csv` with `LookbackEndScore`, `PeriodEndScore`, `ScoreChange`, health classification
3. Weighted average thesis health; % in strong/improving/neutral/weak theses
4. **Figure 2 — Thesis Exposure vs Market Health quadrant** (x = `PeriodEndWeightPct / 100`, y = `PeriodEndScore / 100`)

**When `thematic: false`:**

1. Factual sector/factor health proxies for owned categories
2. **Figure 2 — Top Category Weights** (not thesis-health quadrant)

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

- `ThesisHealth.csv`, `ExposureHealth.csv` (thematic)
- Report sections 6–8 (thematic) or 7 (non-thematic)

## Used by

- `layer3-playbooks/aggregate-state-review`