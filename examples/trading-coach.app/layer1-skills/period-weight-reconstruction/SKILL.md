---
name: period-weight-reconstruction
description: Reconstruct period boundary holdings weights
sourceCorpus:
  repository: trading-coach
  path: capabilities/period-weight-reconstruction/
  readOnly: true
metadata:
  legacyCapabilityKind: analyze
---

Follow **Period Holdings Weight Reconstruction** in `contracts/datastore-contract.md`.

1. For each boundary (`analysisPeriodStart`, `analysisPeriodEnd`): apply observed snapshot or reconstruct backward/forward
2. Record `PeriodStartWeightSource` and `PeriodEndWeightSource`
3. Do not mark weights `unavailable` until reconstruction is attempted
4. Do not substitute a post-period reference snapshot without explicit non-period labeling

Calculate at each boundary: total live account value; invested MV; total liquidity and liquidity %; symbol-level holdings MV.

## Outputs

- Boundary holdings state for downstream capabilities
- Weight source labels for Manifest and Appendix D

## Used by

- `layer3-playbooks/aggregate-state-review` (before `portfolio-weights-table`)