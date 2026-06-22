---
name: holdings-standards-map
description: TradingCoach skill: holdings-standards-map
sourceCorpus:
  repository: trading-coach
  path: capabilities/holdings-standards-map/
  readOnly: true
metadata:
  legacyCapabilityKind: transform
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

## Outputs

- `HoldingsMap.csv`

## CSV schema — HoldingsMap.csv

```text
Symbol,AssetClass,AssetSubclass,GICSSector,GICSIndustry,StyleBucket,LiquidityRole,MappingConfidence,MappingSource,Notes
```

## Used by

- `layer3-playbooks/aggregate-state-review`