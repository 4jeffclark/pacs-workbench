# TradingCoach User Datastore Layout

This pack owns its datastore layout. Bind `userDatastore` to a host directory; use this structure beneath it (legacy TradingCoach `data/` and `reports/` layout).

```text
{userDatastore}/
  data/
    raw/etrade/
    canonical/
    knowledge/
  reports/
  inputs/
```

# TradingCoach Data Store

Persistent user-provided E*TRADE input data used by all treatments.

This repository is single-user, so all data in this store is relevant to future analysis requests unless a treatment explicitly narrows the analysis period or account scope.

## Layout

```text
data/
  raw/
    etrade/
      account_history/
      balances/
      orders/
      portfolio_lot_level/
  canonical/
    accounts.csv
    account_history.csv
    balances.csv
    cash.csv
    cash_activity_daily.csv
    cash_balance_estimated.csv
    income_events.csv
    orders.csv
    positions_lot_level.csv
    ingestion_manifest.csv
  knowledge/
    holdings/
    themes/
    theses/
    policies/
    market/
    {userDatastore}/reports/
    analytics/
```

## Raw Data

`{userDatastore}/data/raw/etrade/` stores immutable native E*TRADE exports exactly as provided by the user.

Raw files are source-of-truth artifacts. Do not edit them after ingestion. If a better export is provided later, ingest it as an additional raw file.

## Canonical Data

`{userDatastore}/data/canonical/` stores normalized CSV tables derived from raw exports. These files are maintained according to `../contracts/datastore-contract.md` and are intended to be easy for agents and humans to inspect.

Canonical files are derived, not authoritative. If raw and canonical data disagree, preserve the raw file and improve the interpretation procedure.

## Persistent Knowledge

`{userDatastore}/data/knowledge/` stores durable portfolio knowledge that future executions should inherit, but which is not fully derivable from broker raw inputs alone.

See `../contracts/persistent-knowledge-model.md`.

Examples:

- confirmed holdings classifications
- evolving theme registries and symbol assignments
- evolving thesis registries and symbol assignments
- reusable policy preferences
- reusable proxy selections
- report lineage and knowledge-promotion history

Knowledge files are distinct from both raw source inputs and rebuildable canonical tables:

- raw files are immutable source truth
- canonical files are deterministic factual transforms
- knowledge files are durable, versioned portfolio memory

## Export Types

Supported initial E*TRADE export types:

- `balances`: account-level balance snapshot.
- `account_history`: account-level statement activity, including trades, dividends, interest, transfers, sweeps, and fees.
- `orders`: historical order records.
- `portfolio_lot_level`: current open positions and lot-level or position-level acquisition metadata.

## Account Identity

E*TRADE exports identify accounts inconsistently:

- `balances` and `portfolio_lot_level` use masked labels such as `Traditional IRA - x7232`.
- `orders` uses full numeric account ids such as `120447232`.

Canonical files normalize the available identifiers:

```text
AccountId
MaskedAccount
AccountLabel
AccountType
```

Where possible, accounts are joined by matching the last four digits of `AccountId` to the masked account token.

## Cash Handling

Cash is not modeled as a position. Canonical cash data stores distinct cash concepts separately:

- `CashAvailToWithdraw`
- `CashBuyingPower`
- `MarginBuyingPower`
- `PortfolioCashOnDeposit`

These values may differ because E*TRADE uses different definitions across exports.

Account history exports improve cash reconstruction but are not historical balance snapshots. Observed balances remain in `cash.csv` and `balances.csv`; derived daily cash activity and estimated cash balances live in `cash_activity_daily.csv` and `cash_balance_estimated.csv`.

## Incremental Merge

The datastore is cumulative. When the user supplies new E*TRADE exports:

1. Hash each file and skip raw copies that already exist.
2. Append new raw files under `{userDatastore}/data/raw/etrade/`.
3. Rebuild all canonical tables from **all** raw files.
4. Merge overlapping exports with deduplication rather than replacing prior data.
5. Validate the rebuilt canonical tables before period selection.

E*TRADE order and account-history exports often overlap prior downloads but may also omit older rows. A merge must preserve older-only rows while deduplicating overlapping activity. Balance and portfolio lot-level exports are kept as separate snapshots.

See `../contracts/datastore-contract.md` → **Incremental Merge and Rebuild** for dedup keys, conflict rules, and validation checks.

## Promotion from Reports

Report folders are the execution-local archive for a single run and are **fully tracked in git** (all markdown, CSV, PDF, and `SourceData/` files). They are not the primary long-term *knowledge* system — confirmed semantic state is promoted into `{userDatastore}/data/knowledge/`.

Structured, reusable, user-confirmed knowledge may be promoted from a report into `{userDatastore}/data/knowledge/` when the relevant playbook and capability contracts allow it.

Examples of likely promotions:

- confirmed `HoldingsMap.csv`
- confirmed `ThemeRegistry.csv` and `ThemeMap.csv`
- confirmed `ThesisRegistry.csv` and `ThesisAssignment.csv`

Examples that usually remain report-local:

- `Report.md`
- `Interview.md`
- `MarketResearch.md`
- period-specific `Metrics.csv`
- period-specific exposure and rotation tables

## Period Handshake

Treatment entry interviews use the combined canonical data store plus any newly provided files to determine the available analysis range. If new files are supplied, the agent must follow `../contracts/datastore-contract.md` to merge non-duplicate raw data, rebuild canonical tables, validate the result, and only then ask the user to choose the full range or a subset.
