# Unit Decision Review Playbook

## Playbook Version

1.1.0

## Playbook Id

unit-decision-review

## Playbook Report Id

UnitDecisionReview

## Product Id

trading-coach

## ASP Manifest

[unit-decision-review.asp.yaml](unit-decision-review.asp.yaml)

## Composition

```text
requires:
  - layer0-workflows/datastore-merge-and-validate
  - layer0-workflows/structured-input-discovery
  - layer0-workflows/period-scope-confirmation
uses:
  - layer1-skills/symbol-trading-analysis       when reviewFocus: lifecycle
  - layer1-skills/stale-position-hygiene        when reviewFocus: stale
  - layer1-skills/event-trade-context           when reviewFocus: event
embeds:
  - layer1-skills/market-environment          optional
overlays:
  - overlays/trade-evaluation.asp.yaml         when evaluation: true
```

## Primary Objective

Forensic review of a specific trade or position decision.

## Inputs

```text
unit-decision-review(
  evaluation: boolean,
  reviewFocus: lifecycle | stale | event,
  eventType?: string,
  targetSymbol: symbol,
  analysisPeriodStart: YYYYMMDD,
  analysisPeriodEnd: YYYYMMDD,
  brokerOrderExport: file | canonical,
  ...
)
```

| `reviewFocus` | Capability |
|---|---|
| `lifecycle` (default) | `symbol-trading-analysis` |
| `stale` | `stale-position-hygiene` |
| `event` | `event-trade-context` |

## Output modes

Core vs augmented per `evaluation` lens (see `PROJECT.md` **ASP Output Modes**).

## Core Output Phase

Run the capability matching `reviewFocus`. Optional embedded `market-environment`.

## Augmented Output Phase

When `evaluation: true`: see [overlays/trade-evaluation.md](overlays/trade-evaluation.md).

## Output Artifacts

```text
{userDatastore}/reports/<GenerationTimestamp>-UnitDecisionReview-<AnalysisStart>-<AnalysisEnd>/
```

Legacy routes: `PositionLifecycle`, `StalePositionReview`, `IPOTrading`.
