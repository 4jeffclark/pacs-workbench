---
name: theme-map-inference
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: theme-map-inference
metadata:
  legacyCapabilityKind: transform
  sourcePath: capabilities/theme-map-inference
  sourceRepository: trading-coach
---

1. Start from confirmed or inferred `HoldingsMap.csv`.
2. Propose a concise theme registry for the current portfolio, typically 3 to 8 active themes.
3. Use external theme namespaces where they materially help, for example `MSCI-TES`; otherwise use `CUSTOM`.
4. Assign each covered symbol one primary `ThemeId`.
5. Leave pure liquidity rows and truly non-thematic residual holdings outside the theme map when appropriate.
6. Record `MappingConfidence` and concise notes for ambiguous assignments.
7. Write `ThemeRegistry.csv` and `ThemeMap.csv`.
8. Route to `theme-map-confirmation` before quantification.

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --input-dir "$AGENT_WORKSPACE/holdings-standards-map"
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

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