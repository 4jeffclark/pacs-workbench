---
name: datastore-inventory
description: TradingCoach skill: datastore-inventory
sourceCorpus:
  repository: trading-coach
  path: capabilities/datastore-inventory/
  readOnly: true
metadata:
  legacyCapabilityKind: retrieve
---

### Step 1 — Inventory the datastore

Raw files by type, canonical tables, row counts, date ranges, account coverage, hashes, truncation risk, missing export types.

### Step 2 — Profile account coverage

Per account: activity ranges, latest snapshots, row counts, gaps, symmetry across accounts.

### Step 3 — Profile activity coverage

Orders, fills, notional by period, top symbols, account-history activity types, open positions.

### Step 4 — Profile cash and income history

Observed cash, account-history activity, estimated cash curves; document confidence layers.

### Step 5 — Profile derived data quality

Normalization, parsing quality, duplicate detection, provenance; label Observed / Derived / Estimated / Low Confidence.

## Outputs

- `DataStoreInventory.csv`, `AccountCoverage.csv`, `Metrics.csv`
- Report quantification sections 1–5

## Used by

- `layer3-playbooks/source-profile`