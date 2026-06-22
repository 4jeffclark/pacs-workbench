---
name: theme-map-confirmation
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: theme-map-confirmation
metadata:
  legacyCapabilityKind: interact
  sourcePath: capabilities/theme-map-confirmation
  sourceRepository: trading-coach
---

1. Present the candidate `ThemeRegistry` with labels, namespaces, and parent groups.
2. Present the proposed `ThemeMap` with member securities, weights, and confidence.
3. Show residual symbols that remain outside the theme map and explain whether they are liquidity or non-thematic residual exposures.
4. Ask the user to confirm, merge, split, rename, or reassign themes.
5. Do not auto-confirm from execution prompt text alone.
6. Store verbatim Q&A in `MappingDiscovery.md` and embed the operative transcript in `Report.md` Appendix A.
7. Completion: `Theme map confirmed.` only after explicit user approval.

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

- Confirmed `ThemeRegistry.csv`
- Confirmed `ThemeMap.csv`
- `MappingDiscovery.md`
- Gate: `theme-map-confirmed`

## Used by

- `layer3-playbooks/aggregate-state-review`