---
name: thesis-registry-confirmation
description: TradingCoach skill: thesis-registry-confirmation
sourceCorpus:
  repository: trading-coach
  path: capabilities/thesis-registry-confirmation/
  readOnly: true
metadata:
  legacyCapabilityKind: interact
---

1. Present candidate theses with thesis statements, parent themes, horizons, catalysts, and status.
2. Present proposed `ThesisAssignment` coverage with member securities, weights, and confidence.
3. Show symbols intentionally outside thesis coverage, including residual buckets and liquidity holdings.
4. Ask the user to merge, split, rename, reassign, close, or invalidate theses.
5. Do not auto-confirm from execution prompt text alone.
6. Store verbatim Q&A in `MappingDiscovery.md` and embed the operative transcript in `Report.md` Appendix A.
7. Completion: `Thesis registry confirmed.` only after explicit user approval.

## Outputs

- Confirmed `ThesisRegistry.csv`
- Confirmed `ThesisAssignment.csv`
- `MappingDiscovery.md`
- Gate: `thesis-registry-confirmed`

## Used by

- `layer3-playbooks/aggregate-state-review`