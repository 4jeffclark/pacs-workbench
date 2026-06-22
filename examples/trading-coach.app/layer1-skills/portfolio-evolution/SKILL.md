---
name: portfolio-evolution
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: portfolio-evolution
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/portfolio-evolution
  sourceRepository: trading-coach
---

1. Compute buy/sell/net notional for the analysis period
2. **When `thematic: true`:** map through `ThesisMap.csv`; produce `ThesisEvolution.csv`, `ThesisRotationMatrix.csv`
3. **When `thematic: false`:** map through `CategoryMap.csv`; produce `CategoryEvolution.csv`, `CategoryRotationMatrix.csv`
4. Report Sections 9–10 (thematic) or 8–9 (non-thematic)

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --period-start YYYYMMDD --period-end YYYYMMDD --thematic true
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- Evolution and rotation CSVs
- Rotation analysis narrative
- Embed complete rotation matrix in `Report.md` Appendix G (non-thematic) or treatment-specified appendix — not a sibling-file pointer

## CSV schemas

**ThesisEvolution.csv:** `ThesisId,PeriodStartWeightPct,PeriodEndWeightPct,BuyNotional,SellNotional,NetFlow,GrossTurnover`

**CategoryEvolution.csv:** `Category,PeriodStartWeightPct,PeriodEndWeightPct,BuyNotional,SellNotional,NetFlow,GrossTurnover`

## Used by

- `layer3-playbooks/aggregate-state-review`