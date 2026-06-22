---
name: thesis-registry-inference
description: TradingCoach skill: thesis-registry-inference
sourceCorpus:
  repository: trading-coach
  path: capabilities/thesis-registry-inference/
  readOnly: true
metadata:
  legacyCapabilityKind: transform
---

1. Start from confirmed `HoldingsMap.csv` and proposed `ThemeMap.csv`.
2. Infer candidate theses using investor intent, catalyst, expected outcome, and time horizon.
3. Require each thesis to include a plain-language statement and a parent `ThemeId`.
4. Assign covered symbols one primary `ThesisId` where an active hypothesis exists.
5. Allow symbols to remain outside the thesis registry when they are residual exposures or pure liquidity.
6. Record `AssignmentConfidence` and concise notes for ambiguity.
7. Write `ThesisRegistry.csv` and `ThesisAssignment.csv`.
8. Route to `thesis-registry-confirmation` before quantification.

## Outputs

- `ThesisRegistry.csv`
- `ThesisAssignment.csv`

## CSV schema — ThesisRegistry.csv

```text
ThesisId,ThesisStatement,ParentThemeId,HorizonStart,HorizonEnd,PrimaryCatalyst,Status,Notes
```

## CSV schema — ThesisAssignment.csv

```text
Symbol,ThesisId,AssignmentConfidence,PrimaryFlag,Notes
```

## Used by

- `layer3-playbooks/aggregate-state-review`