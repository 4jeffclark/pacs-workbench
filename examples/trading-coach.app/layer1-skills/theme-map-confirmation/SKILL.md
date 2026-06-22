---
name: theme-map-confirmation
description: TradingCoach skill: theme-map-confirmation
sourceCorpus:
  repository: trading-coach
  path: capabilities/theme-map-confirmation/
  readOnly: true
metadata:
  legacyCapabilityKind: interact
---

1. Present the candidate `ThemeRegistry` with labels, namespaces, and parent groups.
2. Present the proposed `ThemeMap` with member securities, weights, and confidence.
3. Show residual symbols that remain outside the theme map and explain whether they are liquidity or non-thematic residual exposures.
4. Ask the user to confirm, merge, split, rename, or reassign themes.
5. Do not auto-confirm from execution prompt text alone.
6. Store verbatim Q&A in `MappingDiscovery.md` and embed the operative transcript in `Report.md` Appendix A.
7. Completion: `Theme map confirmed.` only after explicit user approval.

## Outputs

- Confirmed `ThemeRegistry.csv`
- Confirmed `ThemeMap.csv`
- `MappingDiscovery.md`
- Gate: `theme-map-confirmed`

## Used by

- `layer3-playbooks/aggregate-state-review`