---
name: period-weight-reconstruction
compatibility: Requires Python 3.11+ when running bundled scripts
description: Reconstruct period boundary holdings weights
metadata:
  legacyCapabilityKind: analyze
  sourcePath: capabilities/period-weight-reconstruction
  sourceRepository: trading-coach
---

Follow **Period Holdings Weight Reconstruction** in `contracts/datastore-contract.md`.

1. For each boundary (`analysisPeriodStart`, `analysisPeriodEnd`): apply observed snapshot or reconstruct backward/forward
2. Record `PeriodStartWeightSource` and `PeriodEndWeightSource`
3. Do not mark weights `unavailable` until reconstruction is attempted
4. Do not substitute a post-period reference snapshot without explicit non-period labeling

Calculate at each boundary: total live account value; invested MV; total liquidity and liquidity %; symbol-level holdings MV.

## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE" --period-start YYYYMMDD --period-end YYYYMMDD
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.

## Outputs

- Boundary holdings state for downstream capabilities
- Weight source labels for Manifest and Appendix D

## Used by

- `layer3-playbooks/aggregate-state-review` (before `portfolio-weights-table`)