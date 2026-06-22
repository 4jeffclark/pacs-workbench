# Environment Review Playbook

## Playbook Version

1.0.0

## Playbook Id

environment-review

## Playbook Report Id

EnvironmentReview

## Product Id

trading-coach

## Role

Market regime analyst reviewing macro and sector context for a confirmed period and optional portfolio linkage.

## Primary Objective

Answer: *What market regime applies, and how does it interact with positions or thesis?*

## Composition

```text
requires:
  - layer0-workflows/datastore-merge-and-validate
  - layer0-workflows/structured-input-discovery
  - layer0-workflows/period-scope-confirmation
uses:
  - layer1-skills/market-environment
```

## Inputs

```text
environment-review(
  sessionAttachments?: file[],
  dataStore: DataStore,
  evaluation: boolean,
  marketDepth: summary | full,
  analysisPeriodStart: YYYYMMDD,
  analysisPeriodEnd: YYYYMMDD,
  lookbackStart?: YYYYMMDD,
  lookbackEnd?: YYYYMMDD,
  portfolioSymbols?: text,
  thesisList?: text,
  marketProxyList?: text,
  marketFlowSources?: text
)
```

| Parameter | Default | Effect |
|---|---|---|
| `marketDepth` | `full` | `summary` = abbreviated memo; `full` = standalone EnvironmentReview report |
| `evaluation` | `true` | quantification-only vs judgment on regime interpretation |

## Required First Response

```text
TradingCoach Framework

Product: trading-coach
Playbook Selected: Environment Review
Playbook Id: environment-review
Playbook Version: 1.0.0
Asp Schema Version: 1.0
Phase: Input Validation
```

## Quantification Phase

1. Broad regime across lookback, analysis, and follow-through windows
2. Sector/factor performance proxies relevant to owned symbols or thesis list when supplied
3. Volatility, rates, credit, and flow context
4. Record in `MarketResearch.md` and embed key findings in `Report.md`

## Output Artifacts

```text
{userDatastore}/reports/<GenerationTimestamp>-EnvironmentReview-<AnalysisStart>-<AnalysisEnd>/
```

Always: `Manifest.md`, `Report.md`, `MarketResearch.md`, `InputSummary.md`, `Metrics.csv`

When `evaluation: true`: `Interview.md`, `ExitInterview.md`

## Embedded use

When `aggregate-state-review` embeds market-environment, produce summary sections only. When user requests full depth, `references` this playbook and may run standalone.

## Manifest Metadata

```text
Product Id: trading-coach
Playbook Id: environment-review
Playbook Report Id: EnvironmentReview
Market Depth: summary | full
```
