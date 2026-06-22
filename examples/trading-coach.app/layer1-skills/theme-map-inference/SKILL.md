---
name: theme-map-inference
description: TradingCoach skill: theme-map-inference
sourceCorpus:
  repository: trading-coach
  path: capabilities/theme-map-inference/
  readOnly: true
metadata:
  legacyCapabilityKind: transform
---

1. Start from confirmed or inferred `HoldingsMap.csv`.
2. Propose a concise theme registry for the current portfolio, typically 3 to 8 active themes.
3. Use external theme namespaces where they materially help, for example `MSCI-TES`; otherwise use `CUSTOM`.
4. Assign each covered symbol one primary `ThemeId`.
5. Leave pure liquidity rows and truly non-thematic residual holdings outside the theme map when appropriate.
6. Record `MappingConfidence` and concise notes for ambiguous assignments.
7. Write `ThemeRegistry.csv` and `ThemeMap.csv`.
8. Route to `theme-map-confirmation` before quantification.

## Outputs

- `ThemeRegistry.csv`
- `ThemeMap.csv`

## CSV schema — ThemeRegistry.csv

```text
ThemeId,ThemeLabel,ThemeNamespace,ExternalThemeCode,ParentThemeGroup,Description,Status
```

## CSV schema — ThemeMap.csv

```text
Symbol,ThemeId,MappingConfidence,PrimaryFlag,Notes
```

## Used by

- `layer3-playbooks/aggregate-state-review`