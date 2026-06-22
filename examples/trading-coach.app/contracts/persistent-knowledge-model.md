# Persistent Knowledge Model

Canonical persistence model for TradingCoach beyond raw broker inputs and rebuildable canonical tables.

This document defines what should persist as reusable portfolio knowledge, what should remain execution-local in report folders, and how report-generated data may be promoted into durable state.

## Purpose

TradingCoach needs more than a raw input store and a report archive.

Future executions should be able to inherit:

- confirmed symbol classifications
- evolving theme definitions
- evolving thesis definitions
- historical changes in those definitions
- reusable proxy selections
- reusable policy preferences
- report lineage

At the same time, not every report-generated file should become part of the durable datastore.

This contract separates those concerns.

## Four persistence tiers

### Tier 1 — Immutable source inputs

Location:

```text
{userDatastore}/data/raw/
```

Purpose:

- preserve source exports exactly as supplied
- keep an append-only audit trail

Examples:

- broker balances export
- broker orders export
- broker account history export
- broker portfolio lot-level export

Rules:

1. Append-only.
2. Never edited after ingestion.
3. Remain authoritative when canonical interpretation is wrong.

### Tier 2 — Rebuildable canonical factual store

Location:

```text
{userDatastore}/data/canonical/
```

Purpose:

- normalize factual market and account state from raw inputs
- support deterministic analysis workflows

Examples:

- `orders.csv`
- `balances.csv`
- `positions_lot_level.csv`
- `cash_balance_estimated.csv`

Rules:

1. Fully rebuildable from raw inputs and deterministic transformation rules.
2. Must not contain user judgment that cannot be reconstructed.
3. If a canonical interpretation changes, rebuild from raw rather than hand-editing the canonical files.

### Tier 3 — Persistent portfolio knowledge

Location:

```text
{userDatastore}/data/knowledge/
```

Purpose:

- store reusable, durable portfolio knowledge
- preserve user-confirmed semantic state across executions
- track the evolution of themes, theses, policies, and confirmed mappings over time

Examples:

- holdings classifications
- theme registry and symbol assignments
- thesis registry and symbol assignments
- reusable proxy definitions
- target allocation policies
- report lineage registry

Rules:

1. Not fully derivable from broker raw inputs alone.
2. May include user-authored or user-confirmed judgment.
3. Should be versioned or historized when meaning can change over time.
4. Should be reusable by future executions without rediscovery.

### Tier 4 — Execution-local report artifacts

Location:

```text
{userDatastore}/reports/<GenerationTimestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>/
```

Purpose:

- preserve per-run evidence, narrative, and derived outputs
- keep historical reports self-contained and immutable

**Git tracking:** report folders are fully version-controlled. All markdown, CSV, PDF, and `SourceData/` artifacts in a report folder must be committed to git. See `contracts/report-artifact-contract.md` and `AGENT_GIT_PROTOCOL.md`.

Examples:

- `Report.md`
- `Interview.md`
- `ExitInterview.md`
- `MarketResearch.md`
- `Metrics.csv`
- period exposure and rotation CSVs

Rules:

1. Historical reports remain immutable.
2. Report artifacts do not become durable knowledge automatically.
3. Promotion to `{userDatastore}/data/knowledge/` must follow the rules in this document.

## Durable versus execution-local rule

Use this question:

> Should future executions inherit this as current or historical portfolio understanding?

If yes, persist it in `{userDatastore}/data/knowledge/`.

If no, keep it in the report folder.

## `{userDatastore}/data/knowledge/` layout

```text
data/
  knowledge/
    holdings/
    themes/
    theses/
    policies/
    market/
    {userDatastore}/reports/
    analytics/
```

The exact file list may expand, but new durable portfolio-memory artifacts should live under one of these domains.

## Holdings knowledge

### Purpose

Store reusable symbol-level portfolio classifications and liquidity intent.

### Canonical current-state files

```text
{userDatastore}/data/knowledge/holdings/HoldingsMapCurrent.csv
{userDatastore}/data/knowledge/holdings/LiquidityIntentCurrent.csv
```

### Canonical history files

```text
{userDatastore}/data/knowledge/holdings/HoldingsMapHistory.csv
{userDatastore}/data/knowledge/holdings/LiquidityIntentHistory.csv
```

### `HoldingsMapCurrent.csv`

Suggested schema:

```text
Symbol,AssetClass,AssetSubclass,GICSSector,GICSIndustry,StyleBucket,LiquidityRole,MappingConfidence,MappingSource,Notes,LastConfirmedAt,LastConfirmedSource
```

### `HoldingsMapHistory.csv`

Suggested schema:

```text
Symbol,AssetClass,AssetSubclass,GICSSector,GICSIndustry,StyleBucket,LiquidityRole,MappingConfidence,MappingSource,Notes,EffectiveStart,EffectiveEnd,ChangedAt,ChangeReason,ChangedSource
```

### Persistence rule

Promote confirmed holdings classifications into `{userDatastore}/data/knowledge/holdings/` after mapping confirmation. A report-local `HoldingsMap.csv` remains the per-run snapshot; the knowledge layer stores the latest accepted state and its history.

## Theme knowledge

### Purpose

Store durable structural themes and their symbol assignments.

### Canonical files

```text
{userDatastore}/data/knowledge/themes/ThemeRegistry.csv
{userDatastore}/data/knowledge/themes/ThemeMapCurrent.csv
{userDatastore}/data/knowledge/themes/ThemeMapHistory.csv
```

### `ThemeRegistry.csv`

Suggested schema:

```text
ThemeId,ThemeLabel,ThemeNamespace,ExternalThemeCode,ParentThemeGroup,Description,Status,CreatedAt,RetiredAt,CreatedSource
```

### `ThemeMapCurrent.csv`

Suggested schema:

```text
Symbol,ThemeId,AssignmentConfidence,PrimaryFlag,Notes,LastConfirmedAt,LastConfirmedSource
```

### `ThemeMapHistory.csv`

Suggested schema:

```text
Symbol,ThemeId,AssignmentAction,PrimaryFlag,Notes,EffectiveStart,EffectiveEnd,ChangedAt,ChangeReason,ChangedSource
```

### Persistence rule

Promote confirmed themes and symbol assignments after theme confirmation. Theme history is first-class durable knowledge because theme framing evolves over time and should be reusable by future executions.

## Thesis knowledge

### Purpose

Store time-bound investment hypotheses, their lifecycle, and their symbol assignments.

### Canonical files

```text
{userDatastore}/data/knowledge/theses/ThesisRegistry.csv
{userDatastore}/data/knowledge/theses/ThesisAssignmentCurrent.csv
{userDatastore}/data/knowledge/theses/ThesisAssignmentHistory.csv
{userDatastore}/data/knowledge/theses/ThesisEvents.csv
```

### `ThesisRegistry.csv`

Suggested schema:

```text
ThesisId,ThesisStatement,ParentThemeId,HorizonStart,HorizonEnd,PrimaryCatalyst,Status,CreatedAt,ClosedAt,InvalidatedAt,OriginReportId,Notes
```

### `ThesisAssignmentCurrent.csv`

Suggested schema:

```text
Symbol,ThesisId,AssignmentConfidence,PrimaryFlag,Notes,LastConfirmedAt,LastConfirmedSource
```

### `ThesisAssignmentHistory.csv`

Suggested schema:

```text
Symbol,ThesisId,AssignmentAction,PrimaryFlag,Notes,EffectiveStart,EffectiveEnd,ChangedAt,ChangeReason,ChangedSource
```

### `ThesisEvents.csv`

Suggested schema:

```text
ThesisId,EventType,EventDate,SourceReportId,Summary,Notes
```

Canonical `EventType` examples:

- `created`
- `refined`
- `split`
- `merged`
- `closed`
- `invalidated`
- `reopened`

### Persistence rule

Promote confirmed thesis state after thesis confirmation. Thesis evolution should never depend only on past report prose. Store it as structured durable knowledge.

## Policy knowledge

### Purpose

Store reusable user preferences, target rules, and portfolio operating policies.

### Canonical files

```text
{userDatastore}/data/knowledge/policies/PortfolioPolicies.csv
{userDatastore}/data/knowledge/policies/ReviewPreferences.csv
```

### `PortfolioPolicies.csv`

Suggested content:

- target cash floor
- max single-name weight
- acceptable concentration ranges
- default liquidity treatment for certain instruments
- target allocation policy
- rebalancing guardrails

Suggested schema:

```text
PolicyKey,PolicyValue,Scope,EffectiveStart,EffectiveEnd,LastConfirmedAt,Source,Notes
```

### `ReviewPreferences.csv`

Suggested content:

- preferred default `rollupLens`
- preferred default `evaluation` mode
- preferred appendix depth
- preferred lookback or follow-through defaults
- preferred use of prior confirmed maps

Suggested schema:

```text
PreferenceKey,PreferenceValue,Scope,EffectiveStart,EffectiveEnd,LastConfirmedAt,Source,Notes
```

### Persistence rule

Persist only explicit user preferences or clearly confirmed defaults. Do not infer durable policy from a single run unless the user confirms it.

## Market knowledge

### Purpose

Persist reusable proxy selections and market linkage definitions without persisting one-off market narratives as canonical truth.

### Canonical files

```text
{userDatastore}/data/knowledge/market/ProxyRegistry.csv
{userDatastore}/data/knowledge/market/ProxySetMembership.csv
```

### `ProxyRegistry.csv`

Suggested schema:

```text
ProxySetId,ScopeType,ScopeId,ProxySetLabel,Description,Status,CreatedAt,RetiredAt,Source
```

### `ProxySetMembership.csv`

Suggested schema:

```text
ProxySetId,ProxySymbol,Weight,Role,Notes,EffectiveStart,EffectiveEnd,ChangedAt,ChangedSource
```

Examples:

- theme proxy baskets
- thesis proxy baskets
- sector proxy lists
- risk proxy lists

### Persistence rule

Persist reusable proxy definitions. Do not persist period-specific market commentary as canonical knowledge.

## Report knowledge

### Purpose

Track report lineage and what report-derived knowledge was promoted into durable state.

### Canonical files

```text
{userDatastore}/data/knowledge/reports/ReportRegistry.csv
{userDatastore}/data/knowledge/reports/KnowledgePromotions.csv
```

### `ReportRegistry.csv`

Suggested schema:

```text
ReportId,PlaybookId,PlaybookReportId,GenerationTimestamp,AnalysisStart,AnalysisEnd,OutputMode,RollupLens,ReportPath,Status,SupersedesReportId,Notes
```

### `KnowledgePromotions.csv`

Suggested schema:

```text
ReportId,ArtifactType,SourceArtifactPath,TargetKnowledgePath,PromotedAt,PromotionStatus,Notes
```

### Persistence rule

Every promoted durable artifact should have lineage back to the report or interaction where it was confirmed.

## Analytics history

### Purpose

Store compact longitudinal metrics when cross-report time series are useful.

### Canonical files

```text
{userDatastore}/data/knowledge/analytics/ReportMetricsHistory.csv
```

### Examples

- thesis health score over time
- sector concentration over time
- liquidity ratio over time
- evaluation score over time

### Persistence rule

This layer is optional and secondary. It should not replace report-local metrics or the primary knowledge objects above.

## What should normally stay report-local (not promoted to knowledge)

These artifacts usually remain in their report folders and are **not auto-promoted** into `{userDatastore}/data/knowledge/`. They are still **committed to git** with the report folder.

- `Report.md`
- `Report.pdf`
- `Interview.md`
- `ExitInterview.md`
- `MarketResearch.md`
- `InputSummary.md`
- period-specific `Metrics.csv`
- period-specific exposure tables
- period-specific evolution and rotation tables
- scorecards and verdicts

Reason:

- they are specific to one execution
- they are often recomputable
- they are usually better as evidence than as durable state

## Promotion rules

### Auto-promote

Promote an artifact into `{userDatastore}/data/knowledge/` when all of the following are true:

1. It is structured.
2. It is reusable beyond the current run.
3. It reflects user-confirmed or explicitly accepted state.
4. It is not merely a period-specific derived metric snapshot.

Typical auto-promoted candidates:

- confirmed holdings map
- confirmed theme registry and theme map
- confirmed thesis registry and thesis assignments
- confirmed liquidity intent
- confirmed proxy sets

### Manual or explicit promotion

Require user confirmation before promoting:

- inferred policy preferences
- target allocations
- operating rules
- anything that changes how future runs behave by default

### Keep local by default

Keep report-local when the artifact is:

- narrative
- highly period-dependent
- evidence-heavy
- easy to recompute

## Source Profile playbook role

`source-profile` should eventually inventory not just raw and canonical data, but also durable knowledge health:

- current coverage of `HoldingsMapCurrent`
- active theme count
- active thesis count
- policy coverage
- report registry coverage
- stale knowledge objects needing reconfirmation

This playbook is the natural home for profiling and validating `{userDatastore}/data/knowledge/`.

## Aggregate state review role

`aggregate-state-review` should:

1. load current durable knowledge before asking for re-confirmation
2. use durable knowledge as the starting baseline
3. record changes in report-local artifacts for the run
4. promote confirmed changes back into `{userDatastore}/data/knowledge/`

## Design principles

1. Raw inputs are immutable.
2. Canonical factual tables are rebuildable.
3. Portfolio knowledge is durable and historized.
4. Reports are immutable run artifacts, not the primary memory system.
5. Future executions should inherit confirmed portfolio understanding from `{userDatastore}/data/knowledge/`, not by searching old reports.

## Non-goals

This model does not:

- require every report-local metric to become a knowledge table
- replace report folders as the historical evidence archive
- treat inferred judgment as durable truth without confirmation
- force a single-file implementation for every knowledge domain

## Recommended first implementation targets

Implement in this order:

1. `{userDatastore}/data/knowledge/holdings/`
2. `{userDatastore}/data/knowledge/themes/`
3. `{userDatastore}/data/knowledge/theses/`
4. `{userDatastore}/data/knowledge/reports/`
5. `{userDatastore}/data/knowledge/policies/`
6. `{userDatastore}/data/knowledge/market/`
7. `{userDatastore}/data/knowledge/analytics/` only if cross-report metric history becomes important
