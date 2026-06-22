---
name: holdings-map-confirmation
description: TradingCoach skill: holdings-map-confirmation
sourceCorpus:
  repository: trading-coach
  path: capabilities/holdings-map-confirmation/
  readOnly: true
metadata:
  legacyCapabilityKind: interact
---

1. Present inferred `AssetClass`, `AssetSubclass`, `GICSSector`, `GICSIndustry`, `StyleBucket`, and `LiquidityRole` groupings with member securities where practical.
2. Highlight low-confidence rows and any symbols with blank GICS fields.
3. Ask the user to confirm, merge, split, rename, or recategorize classifications as needed.
4. Explicitly confirm ambiguous liquidity sleeves and any proposed `dual` roles.
5. Do not auto-confirm from execution prompt text alone.
6. Store verbatim Q&A in `MappingDiscovery.md` and embed the operative transcript in `Report.md` Appendix A.
7. Completion: `Holdings map confirmed.` only after explicit user approval.

## Outputs

- Confirmed `HoldingsMap.csv`
- `MappingDiscovery.md`
- Gate: `holdings-map-confirmed`

## Used by

- `layer3-playbooks/aggregate-state-review`