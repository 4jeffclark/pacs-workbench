---
name: thesis-registry-confirmation
compatibility: Requires Python 3.11+ when running bundled scripts
description: TradingCoach skill: thesis-registry-confirmation
metadata:
  legacyCapabilityKind: interact
  sourcePath: capabilities/thesis-registry-confirmation
  sourceRepository: trading-coach
---

1. Present candidate theses with thesis statements, parent themes, horizons, catalysts, and status.
2. Present proposed `ThesisAssignment` coverage with member securities, weights, and confidence.
3. Show symbols intentionally outside thesis coverage, including residual buckets and liquidity holdings.
4. Ask the user to merge, split, rename, reassign, close, or invalidate theses.
5. Do not auto-confirm from execution prompt text alone.
6. Store verbatim Q&A in `MappingDiscovery.md` and embed the operative transcript in `Report.md` Appendix A.
7. Completion: `Thesis registry confirmed.` only after explicit user approval.

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --input-dir "$AGENT_WORKSPACE/thesis-registry-inference"
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- Confirmed `ThesisRegistry.csv`
- Confirmed `ThesisAssignment.csv`
- `MappingDiscovery.md`
- Gate: `thesis-registry-confirmed`

## Used by

- `layer3-playbooks/aggregate-state-review`