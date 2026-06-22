# Aggregate State Review Playbook

## Playbook Version

2.0.0

## Playbook Id

aggregate-state-review

## Playbook Report Id

AggregateStateReview

## Product Id

trading-coach

## ASP Manifest

[aggregate-state-review.asp.yaml](aggregate-state-review.asp.yaml)

## Composition

```text
requires:
  - layer0-workflows/datastore-merge-and-validate
  - layer0-workflows/structured-input-discovery
  - layer0-workflows/period-scope-confirmation
uses:
  - layer1-skills/holdings-standards-map
  - layer1-skills/holdings-map-confirmation
  - layer1-skills/theme-map-inference          when rollupLens: theme | thesis
  - layer1-skills/theme-map-confirmation       when rollupLens: theme | thesis
  - layer1-skills/thesis-registry-inference    when rollupLens: thesis
  - layer1-skills/thesis-registry-confirmation when rollupLens: thesis
  - layer1-skills/portfolio-holdings-state
  - layer1-skills/period-weight-reconstruction
  - layer1-skills/portfolio-weights-table
  - layer1-skills/thesis-health
  - layer1-skills/portfolio-period-flows
  - layer1-skills/portfolio-evolution
  - layer1-skills/portfolio-liquidity-analysis
  - layer1-skills/portfolio-concentration-resilience
embeds:
  - layer1-skills/market-environment
references:
  - layer3-playbooks/environment-review              when full market depth requested
overlays:
  - overlays/portfolio-evaluation.asp.yaml    when evaluation: true
  - overlays/rebalancing-review.asp.yaml      when rebalancingReview: true
  - overlays/risk-review.asp.yaml             when riskReview: true
```

Capability procedures: `layer1-skills/*.md`. Overlay procedures: `overlays/*.md`.

## Role

Portfolio analyst and market researcher reviewing **portfolio state** (not trader activity). When `evaluation: true`, the **evaluation overlay** adds coaching; it is not part of core output.

## Primary Objective

Answer portfolio state and change questions for the confirmed period. See capability outputs for standards, theme, and thesis rollup differences.

When `evaluation: true`, also address whether management decisions improved alignment/construction (evaluation overlay).

## Inputs

```text
aggregate-state-review(
  sessionAttachments?: file[],
  dataStore: DataStore,
  evaluation: boolean,              // ASP: activates evaluation overlay; false = core output only
  rollupLens: standards | theme | thesis,
  compositionReview: boolean,
  rebalancingReview: boolean,
  riskReview: boolean,
  analysisPeriodStart: YYYYMMDD,
  analysisPeriodEnd: YYYYMMDD,
  lookbackStart?: YYYYMMDD,
  lookbackEnd?: YYYYMMDD,
  followThroughStart?: YYYYMMDD,
  followThroughEnd?: YYYYMMDD,
  periodStartSnapshot?: YYYYMMDD,
  periodEndSnapshot?: YYYYMMDD,
  holdingsSnapshot: file | canonical,
  brokerOrderExport?: file | canonical,
  cashData?: file | canonical,
  accountHistory?: file | canonical,
  gainsLossesExport?: file | canonical,
  holdingsMap?: file | text,
  themeRegistry?: file | text,
  themeMap?: file | text,
  thesisRegistry?: file | text,
  thesisAssignment?: file | text,
  cashEquivalentSymbols?: text,
  watchlist?: file | text,
  traderNotes?: text,
  riskPlanOrTargetAllocation?: text,
  priorReports?: file[],
  marketProxyList?: text,
  marketFlowSources?: text
)
```

| Parameter | Default | Notes |
|---|---|---|
| `evaluation` | `true` | `false` → **core output only**; `true` → core + **evaluation overlay** |
| `rollupLens` | `theme` | `standards` = GICS-first, `theme` = structural themes, `thesis` = active hypotheses |
| `compositionReview` | `true` | Mapping and weights (always on for this playbook) |
| `rebalancingReview` | `false` | **Enrichment overlay** |
| `riskReview` | `false` | **Enrichment overlay** |

Resolve all parameters via **Structured Inputs Framework** in `PROJECT.md`. Mapping confirmations use **interact** capabilities — not the evaluation entry interview. Holdings standards confirmation is always required; theme and thesis confirmations are additive by lens. See `contracts/holdings-taxonomy.md`.

## Output modes (ASP)

| Mode | `evaluation` | Overlays active | Deliverable |
|---|---|---|---|
| **Core output** | `false` | none (enrichment overlays may still apply if active) | Quantification report only |
| **Augmented output** | `true` | evaluation (+ enrichment if active) | Core report + interview + scorecard + verdict |

When `evaluation: false`, after Input Discovery say: `Input Discovery complete. Generating quantification report.`

## Required First Response

```text
TradingCoach Framework

Product: trading-coach
Playbook Selected: Aggregate State Review
Playbook Id: aggregate-state-review
Playbook Version: 2.0.0
Asp Schema Version: 1.0
Phase: Input Validation
Output Mode: <core | augmented — pending evaluation lens>

Report generation is prohibited until:

[ ] Data Store Updated
[ ] Holdings Map Confirmed
[ ] Theme Map Confirmed when rollupLens: theme | thesis
[ ] Thesis Registry Confirmed when rollupLens: thesis
[ ] Analysis Period Confirmed
[ ] Market Context Complete
[ ] Entry Interview Complete when evaluation: true
```

## Input Discovery

Follow workflows in order. Playbook-specific steps:

1. After datastore merge: run `holdings-standards-map`
2. Confirm period via `period-scope-confirmation`
3. Run `holdings-map-confirmation`
4. When `rollupLens: theme | thesis`: run `theme-map-inference` then `theme-map-confirmation`
5. When `rollupLens: thesis`: run `thesis-registry-inference` then `thesis-registry-confirmation`
6. Present **Inputs Resolved** (all parameters + mapping gates)

Explicit period model defaults: see `layer0-workflows/period-scope-confirmation.md`.

## Core Output Phase

Run capabilities in order after Input Discovery gates clear:

| Step | Capability | Report sections |
|---|---|---|
| 1 | `portfolio-holdings-state` | — |
| 2 | `period-weight-reconstruction` | Period And Data Scope |
| 3 | `portfolio-weights-table` | Section 3 + Figure 1 |
| 4 | `thesis-health` | Sections 6–8 or 7 depending on `rollupLens` |
| 5 | `portfolio-period-flows` + `portfolio-evolution` | Sections 9–10 |
| 6 | `portfolio-liquidity-analysis` | Section 4 |
| 7 | `portfolio-concentration-resilience` | Section 11 or 10 |
| 8 | `market-environment` (embedded) | Market context + Appendix C |

Validate rendering per **Report.md Rendering Conventions** in `PROJECT.md` (GitHub-safe Mermaid only; table fallback required).

### Pre-finalization checklist

Before declaring the report complete:

1. **Self-containment:** No pointers to sibling files (`MarketResearch.md`, `HoldingsMap.csv`, etc.) for evidence or citations.
2. **Appendix C:** Full inline citations — not a summary pointing elsewhere.
3. **Appendices F+:** Embed complete exposure/rotation tables — not an artifact file index.
4. **Mermaid:** GitHub-safe types only; each figure has a markdown table fallback; note PDF/Mermaid limits in Data Limitations.
5. **No execution scripts:** Do not add repo-owned Python/shell analysis scripts; compute and write artifacts per capability procedures.
6. **Manifest:** Record `Output Mode`, typed layer1-skills/overlays, weight sources.

## Augmented Output Phase

When `evaluation: true`:

1. Complete core output phase first
2. Run `evaluation-entry-interview` (via portfolio-evaluation overlay)
3. Apply overlay judgment sections per [overlays/portfolio-evaluation.md](overlays/portfolio-evaluation.md)
4. When `rebalancingReview: true`: add [overlays/rebalancing-review.md](overlays/rebalancing-review.md) sections
5. When `riskReview: true`: add [overlays/risk-review.md](overlays/risk-review.md) sections
6. Scorecard and verdict per evaluation overlay
7. After user review: `exit-interview`

## Output Artifacts

```text
{userDatastore}/reports/<GenerationTimestamp>-AggregateStateReview-<AnalysisStart>-<AnalysisEnd>/
```

**Always:** `Manifest.md`, `Report.md`, `InputSummary.md`, `MarketResearch.md`, `Metrics.csv`, `HoldingsMap.csv`, `LiquidityBreakdown.csv`

**When `rollupLens: standards`:** `SectorExposure.csv`, `AssetClassExposure.csv`, `StyleBucketExposure.csv`, `SectorEvolution.csv`, `SectorRotationMatrix.csv`

**When `rollupLens: theme`:** `ThemeRegistry.csv`, `ThemeMap.csv`, `ThemeExposure.csv`, `StyleBucketExposure.csv`, `ThemeHealth.csv`, `ThemeEvolution.csv`, `ThemeRotationMatrix.csv`

**When `rollupLens: thesis`:** `ThemeRegistry.csv`, `ThemeMap.csv`, `ThesisRegistry.csv`, `ThesisAssignment.csv`, `ThesisExposure.csv`, `ThemeExposure.csv`, `ThesisHealth.csv`, `ExposureHealth.csv`, `ThesisEvolution.csv`, `ThesisRotationMatrix.csv`

**When any mapping confirmation runs:** `MappingDiscovery.md`

**When `evaluation: true`:** `Interview.md`, `ExitInterview.md`

CSV schemas: defined in owning capabilities under `layer1-skills/`.

## Manifest Metadata

```text
Product Id: trading-coach
Playbook Id: aggregate-state-review
Playbook Report Id: AggregateStateReview
Asp Schema Version: 1.0
Playbook Version: 2.0.0
Output Mode: core | augmented
Workflows Executed: <list>
Capabilities Executed: <list with capabilityKind where helpful>
Overlays Executed: <list with overlayKind>
Rollup Lens: standards | theme | thesis
Composition Review: true | false
Rebalancing Review: true | false
Risk Review: true | false
Period Start Weight Source: ...
Period End Weight Source: ...
Holdings Map Confirmed: ...
Theme Map Confirmed: ...
Thesis Registry Confirmed: ...
```

## Report Section Index

**Core (`rollupLens: theme`):** Quantification Summary → Period Scope → Theme Weights → Liquidity → Theme Health → Evolution → Rotation → Concentration → Data Limitations → Appendices A–H

**Core (`rollupLens: thesis`):** Quantification Summary → Period Scope → Thesis Weights → Liquidity → Thesis Health → Evolution → Rotation → Concentration → Data Limitations → Appendices A–I

**Core (`rollupLens: standards`):** Quantification Summary → Period Scope → Sector Weights → Asset Class And Style → Liquidity → Sector Context → Evolution → Rotation → Concentration → Data Limitations → Appendices A–H

**Appendices (`rollupLens: standards`, core):**

| Appendix | Content |
|---|---|
| A | Verbatim holdings map confirmation transcript + confirmed member lists |
| B | Order-flow evidence note (sector rollups in body; state in D if full order table omitted) |
| C | **Full inline** market research citations |
| D | Calculation notes and reconstruction method |
| E | Exit interview when `evaluation: true`; otherwise N/A |
| F | Complete holdings, asset class, sector, and style exposure tables |
| G | Complete sector rotation matrix |

Do **not** use any appendix as a sibling file manifest or artifact index.

**Augmented:** Executive Summary, assessments, scorecard, verdict, Appendix E (exit interview) — per evaluation overlay

## Playbook Fit Routing

| Question | Lens |
|---|---|
| Portfolio / sector composition | `rollupLens: standards` |
| Thematic portfolio composition | `rollupLens: theme` |
| Thesis portfolio composition | `rollupLens: thesis` |
| Reshaping quality | `rebalancingReview: true` |
| Risk posture | `riskReview: true` |
