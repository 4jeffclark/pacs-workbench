# Workflow — datastore-merge-and-validate

## Workflow Id

`datastore-merge-and-validate`

## Layer

0 — infrastructure

## Purpose

Merge session attachments into the persistent E*TRADE datastore, rebuild canonical tables from all raw exports, validate, and present available date range.

## Procedure

Follow [contracts/datastore-contract.md](../contracts/datastore-contract.md):

1. Hash-check session attachments; skip duplicates already in `{userDatastore}/data/raw/etrade/`
2. Copy new exports to appropriate `{userDatastore}/data/raw/etrade/` subfolders
3. Rebuild all tables under `{userDatastore}/data/canonical/` from **all** raw files (merge, not replace)
4. Deduplicate `orders` and `account_history` per contract keys
5. Validate merged canonical datastore
6. Report `dataStoreRange`, `dataStoreStatus`, and holdings snapshot dates (`AsOfLocal`)

## Outputs

- Updated canonical tables
- Datastore range summary for Input Discovery

## Manifest

See [datastore-merge-and-validate.asp.yaml](datastore-merge-and-validate.asp.yaml)
