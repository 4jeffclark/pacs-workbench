---
name: thesis-registry-inference
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: thesis-registry-inference
metadata:
  legacyCapabilityKind: transform
  sourcePath: capabilities/thesis-registry-inference
  sourceRepository: trading-coach
---

1. Start from confirmed `HoldingsMap.csv` and proposed `ThemeMap.csv`.
2. Infer candidate theses using investor intent, catalyst, expected outcome, and time horizon.
3. Require each thesis to include a plain-language statement and a parent `ThemeId`.
4. Assign covered symbols one primary `ThesisId` where an active hypothesis exists.
5. Allow symbols to remain outside the thesis registry when they are residual exposures or pure liquidity.
6. Record `AssignmentConfidence` and concise notes for ambiguity.
7. Write `ThesisRegistry.csv` and `ThesisAssignment.csv`.
8. Route to `thesis-registry-confirmation` before quantification.

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --input-dir "$AGENT_WORKSPACE/theme-map-inference"
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

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