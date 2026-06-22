---
name: holdings-standards-map
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: holdings-standards-map
metadata:
  legacyCapabilityKind: transform
  sourcePath: capabilities/holdings-standards-map
  sourceRepository: trading-coach
---

1. Build the symbol mapping universe per `PROJECT.md` period-based analysis conventions.
2. Normalize ticker formats before classification.
3. Classify every symbol into `AssetClass` and `AssetSubclass`.
4. Infer `GICSSector` and `GICSIndustry` when the instrument is a company or fund exposure where GICS is meaningful.
5. Assign `StyleBucket` only as a secondary construction label; do not let it replace standards namespaces.
6. Classify `LiquidityRole`, explicitly separating `cash_equivalent`, `broker_cash`, `invested`, and `dual`.
7. Record `MappingSource` and `MappingConfidence` for each row.
8. Write one row per symbol to `HoldingsMap.csv`.
9. Route to `holdings-map-confirmation` before quantification.

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

- `HoldingsMap.csv`

## CSV schema — HoldingsMap.csv

```text
Symbol,AssetClass,AssetSubclass,GICSSector,GICSIndustry,StyleBucket,LiquidityRole,MappingConfidence,MappingSource,Notes
```

## Used by

- `layer3-playbooks/aggregate-state-review`