---
name: holdings-map-confirmation
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: holdings-map-confirmation
metadata:
  legacyCapabilityKind: interact
  sourcePath: capabilities/holdings-map-confirmation
  sourceRepository: trading-coach
---

1. Present inferred `AssetClass`, `AssetSubclass`, `GICSSector`, `GICSIndustry`, `StyleBucket`, and `LiquidityRole` groupings with member securities where practical.
2. Highlight low-confidence rows and any symbols with blank GICS fields.
3. Ask the user to confirm, merge, split, rename, or recategorize classifications as needed.
4. Explicitly confirm ambiguous liquidity sleeves and any proposed `dual` roles.
5. Do not auto-confirm from execution prompt text alone.
6. Store verbatim Q&A in `MappingDiscovery.md` and embed the operative transcript in `Report.md` Appendix A.
7. Completion: `Holdings map confirmed.` only after explicit user approval.

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

- Confirmed `HoldingsMap.csv`
- `MappingDiscovery.md`
- Gate: `holdings-map-confirmed`

## Used by

- `layer3-playbooks/aggregate-state-review`