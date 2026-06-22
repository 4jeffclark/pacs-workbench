# Activity Period Review Playbook

## Playbook Version

1.1.0

## Playbook Id

activity-period-review

## Playbook Report Id

ActivityPeriodReview

## Product Id

trading-coach

## ASP Manifest

[activity-period-review.asp.yaml](activity-period-review.asp.yaml)

## Composition

```text
requires:
  - layer0-workflows/datastore-merge-and-validate
  - layer0-workflows/structured-input-discovery
  - layer0-workflows/period-scope-confirmation
uses:
  - layer1-skills/trading-activity-analysis
embeds:
  - layer1-skills/market-environment
overlays:
  - overlays/activity-evaluation.asp.yaml    when evaluation: true
```

## Primary Objective

Evaluate trading activity over a confirmed day or multi-day period.

## Inputs

```text
activity-period-review(
  sessionAttachments?: file[],
  dataStore: DataStore,
  evaluation: boolean,
  analysisPeriodStart: YYYYMMDD,
  analysisPeriodEnd: YYYYMMDD,
  brokerOrderExport: file | canonical,
  gainsLossesExport?: file | canonical,
  watchlist?: text,
  tradeNotes?: text,
  tradingPlan?: text,
  riskPlan?: text,
  priorReports?: file[]
)
```

| `evaluation` | `false` = core output; `true` = core + **evaluation overlay** |

## Output modes

When `evaluation: false`: `Input Discovery complete. Generating quantification report.`

## Core Output Phase

1. `trading-activity-analysis` — orders, metrics, factual market context
2. `market-environment` (embedded summary)

## Augmented Output Phase

When `evaluation: true`: `evaluation-entry-interview` → execution/opportunity evaluation → scorecard → `exit-interview`. See [overlays/activity-evaluation.md](overlays/activity-evaluation.md).

## Output Artifacts

```text
{userDatastore}/reports/<GenerationTimestamp>-ActivityPeriodReview-<AnalysisStart>-<AnalysisEnd>/
```

`Manifest.md`, `Report.md`, `InputSummary.md`, `MarketResearch.md`, `Metrics.csv`; `Interview.md` / `ExitInterview.md` when augmented.

## Manifest Metadata

Include `Output Mode`, `Capabilities Executed`, `Overlays Executed` (with kinds), standard ASP fields.

Legacy treatment id `DayTrading` routes here.
