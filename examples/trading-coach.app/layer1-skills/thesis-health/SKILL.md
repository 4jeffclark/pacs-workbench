---
name: thesis-health
description: TradingCoach skill: thesis-health
sourceCorpus:
  repository: trading-coach
  path: capabilities/thesis-health/
  readOnly: true
metadata:
  legacyCapabilityKind: analyze
---

**When `thematic: true`:**

1. Per owned thesis: momentum, relative strength, volatility, drawdown, breadth/flow proxies, catalysts
2. `ThesisHealth.csv` with `LookbackEndScore`, `PeriodEndScore`, `ScoreChange`, health classification
3. Weighted average thesis health; % in strong/improving/neutral/weak theses
4. **Figure 2 — Thesis Exposure vs Market Health quadrant** (x = `PeriodEndWeightPct / 100`, y = `PeriodEndScore / 100`)

**When `thematic: false`:**

1. Factual sector/factor health proxies for owned categories
2. **Figure 2 — Top Category Weights** (not thesis-health quadrant)

## Outputs

- `ThesisHealth.csv`, `ExposureHealth.csv` (thematic)
- Report sections 6–8 (thematic) or 7 (non-thematic)

## Used by

- `layer3-playbooks/aggregate-state-review`