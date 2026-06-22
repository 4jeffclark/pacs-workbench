---
name: portfolio-evolution
description: TradingCoach skill: portfolio-evolution
sourceCorpus:
  repository: trading-coach
  path: capabilities/portfolio-evolution/
  readOnly: true
metadata:
  legacyCapabilityKind: analyze
---

1. Compute buy/sell/net notional for the analysis period
2. **When `thematic: true`:** map through `ThesisMap.csv`; produce `ThesisEvolution.csv`, `ThesisRotationMatrix.csv`
3. **When `thematic: false`:** map through `CategoryMap.csv`; produce `CategoryEvolution.csv`, `CategoryRotationMatrix.csv`
4. Report Sections 9–10 (thematic) or 8–9 (non-thematic)

## Outputs

- Evolution and rotation CSVs
- Rotation analysis narrative
- Embed complete rotation matrix in `Report.md` Appendix G (non-thematic) or treatment-specified appendix — not a sibling-file pointer

## CSV schemas

**ThesisEvolution.csv:** `ThesisId,PeriodStartWeightPct,PeriodEndWeightPct,BuyNotional,SellNotional,NetFlow,GrossTurnover`

**CategoryEvolution.csv:** `Category,PeriodStartWeightPct,PeriodEndWeightPct,BuyNotional,SellNotional,NetFlow,GrossTurnover`

## Used by

- `layer3-playbooks/aggregate-state-review`