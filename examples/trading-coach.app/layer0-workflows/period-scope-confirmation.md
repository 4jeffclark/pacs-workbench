# Workflow — period-scope-confirmation

## Workflow Id

`period-scope-confirmation`

## Layer

0 — infrastructure

## Purpose

Confirm analysis period, lookback, follow-through, and snapshot/reconstruction anchors after datastore merge.

## Procedure

Follow **Period-Based Analysis Conventions** in [PROJECT.md](../PROJECT.md):

| Window | Parameters | Default |
|---|---|---|
| Analysis period | `analysisPeriodStart`, `analysisPeriodEnd` | user confirms or full datastore range |
| Lookback | `lookbackStart`, `lookbackEnd` | 4 weeks before analysis start → day before start |
| Follow-through | `followThroughStart`, `followThroughEnd` | day after analysis end → +1 week when data exists |
| Period-end snapshot | `periodEndSnapshot` | latest holdings on/before analysis end or reconstruction anchor |
| Period-start snapshot | `periodStartSnapshot` | latest holdings on/before analysis start or reconstruction anchor |

Present **Entry Interview Question 1** (analysis period) and lookback confirmation when defaults apply.

## Outputs

- Confirmed period parameters in Inputs Resolved
- Weight reconstruction plan summary (when period boundaries lack exact snapshots)

## Manifest

See [period-scope-confirmation.asp.yaml](period-scope-confirmation.asp.yaml)
