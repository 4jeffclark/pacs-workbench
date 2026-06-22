# Holdings Taxonomy

Canonical holdings classification contract for TradingCoach portfolio analysis.

This document replaces ad hoc use of `Category`, `GenericBucket`, and thesis-theme rollups as the organizing model for portfolio reports. New work should target the taxonomy in this file.

For persistence rules across durable portfolio memory versus report-local artifacts, see `contracts/persistent-knowledge-model.md`.

## Purpose

TradingCoach supports multiple portfolio reporting modalities:

- standards-based composition reporting
- thematic composition reporting
- thesis-driven composition reporting
- risk and rebalancing overlays
- cross-playbook enrichment for trade and activity reviews

Those modalities require multiple namespaces that answer different questions. This contract keeps those namespaces separate so reports can change their primary rollup lens without changing the underlying symbol map.

## Core rule

Do not collapse instrument taxonomy, economic exposure, style, liquidity function, theme, and thesis into one or two columns.

Use separate namespaces with explicit ownership:

| Layer | Namespace | Meaning | Owner |
|---|---|---|---|
| L0 | `AssetClass` | Instrument type | external / inferred |
| L1 | `AssetSubclass` | More specific instrument slice | external / inferred |
| L2 | `GICSSector` | Broad economic exposure | external / inferred |
| L3 | `GICSIndustry` | Granular economic exposure | external / inferred |
| L4 | `StyleBucket` | Equity style or regime role | TradingCoach |
| L5 | `LiquidityRole` | Portfolio cash-function role | user-confirmed |
| L6 | `ThemeId` | Structural megatrend exposure | external namespace or user-defined |
| L7 | `ThesisId` | Time-bound investment hypothesis | user-defined |

## Namespace definitions

### Standards namespaces

These are symbol-intrinsic and should be stable across playbooks.

#### `AssetClass`

Top-level instrument taxonomy. Canonical values:

- `Equity`
- `FixedIncome`
- `Commodity`
- `Cash`
- `Alternative`
- `Hybrid`
- `DigitalAsset`
- `Other`

#### `AssetSubclass`

More specific instrument slice. Use concise allocator-style labels such as:

- `US Equity`
- `International Equity`
- `Emerging Markets Equity`
- `REIT Equity`
- `Treasury ETF`
- `Inflation-Protected Treasury ETF`
- `Physical Precious Metal Trust`
- `Broad Market ETF`
- `Factor ETF`
- `Energy Commodity Fund`
- `Digital Asset Fund`

`AssetSubclass` should not be used for style labels such as growth or cyclical.

#### `GICSSector`

Use the standard GICS sector name when applicable. Canonical values today:

- `Communication Services`
- `Consumer Discretionary`
- `Consumer Staples`
- `Energy`
- `Financials`
- `Health Care`
- `Industrials`
- `Information Technology`
- `Materials`
- `Real Estate`
- `Utilities`

Nullable for instruments where GICS does not cleanly apply, such as broker cash or certain commodity trusts.

#### `GICSIndustry`

Use a granular GICS economic label. This may be GICS industry or sub-industry, but the file must be internally consistent for a run. For now TradingCoach uses a single `GICSIndustry` field rather than splitting industry and sub-industry into two columns.

### TradingCoach namespaces

These are pack-owned and may vary by portfolio construction or reporting objective.

#### `StyleBucket`

Secondary construction label for standards-first and residual exposures. Canonical values:

- `Growth`
- `Value`
- `Income`
- `Defensive`
- `Cyclical`
- `IndexFactor`
- `International`
- `Other`

Use `StyleBucket` for residual grouping, not for primary portfolio classification.

#### `LiquidityRole`

Functional liquidity meaning within the portfolio:

- `cash_equivalent`
- `broker_cash`
- `invested`
- `dual`

`LiquidityRole` is never inferred from GICS or theme alone when ambiguity exists. User confirmation is required for `dual` and any sleeve where the same symbol may act as reserve capital and an active thesis position.

### Theme namespace

`ThemeId` represents a structural, reusable megatrend exposure such as AI infrastructure, precious metals, or clean energy.

Themes are not the same as theses:

- a theme is durable and can persist for years
- a thesis is a time-bound hypothesis tied to catalyst, horizon, or expected outcome

Themes belong in a registry so they can be reused across periods.

### Thesis namespace

`ThesisId` represents an active investment hypothesis, for example:

- gold will rally to new highs by Q1 2027
- AI capex leadership persists through the next earnings cycle
- short-duration treasuries are capital waiting for redeployment

Every thesis must have:

- a plain-language statement
- a parent `ThemeId`
- a horizon
- a status

## Primary report lens

TradingCoach portfolio composition should no longer branch on a binary `thematic` flag.

Use:

```text
rollupLens: standards | theme | thesis
```

### `rollupLens: standards`

Primary report axis:

- `GICSSector` plus `Liquidity`

Secondary axes:

- `AssetClass`
- `AssetSubclass`
- `StyleBucket`

### `rollupLens: theme`

Primary report axis:

- `ThemeId` plus residual `StyleBucket` rows and `Liquidity`

Secondary axes:

- standards namespaces in appendices

### `rollupLens: thesis`

Primary report axis:

- `ThesisId` plus `Liquidity`

Secondary axes:

- parent `ThemeId`
- standards namespaces in appendices

## File contracts

### `HoldingsMap.csv`

Required for all aggregate-state-review runs and any other playbook that enriches output with holdings classification.

Schema:

```text
Symbol,AssetClass,AssetSubclass,GICSSector,GICSIndustry,StyleBucket,LiquidityRole,MappingConfidence,MappingSource,Notes
```

Rules:

1. One row per normalized symbol in the mapping universe.
2. `AssetClass` and `LiquidityRole` must always be populated.
3. `GICSSector` and `GICSIndustry` may be blank only when they do not apply cleanly.
4. `MappingSource` records where the classification came from, for example `finnhub`, `fmp`, `issuer_factsheet`, `manual`, `sec_sic`.
5. `Notes` is optional and should stay concise.

Persistence:

- report-local copy: execution snapshot for the current run
- durable promotion target: `{userDatastore}/data/knowledge/holdings/HoldingsMapCurrent.csv` and `HoldingsMapHistory.csv`

### `ThemeRegistry.csv`

Reusable catalog of structural themes.

Schema:

```text
ThemeId,ThemeLabel,ThemeNamespace,ExternalThemeCode,ParentThemeGroup,Description,Status
```

Rules:

1. `ThemeNamespace` identifies the naming system, such as `MSCI-TES` or `CUSTOM`.
2. `ExternalThemeCode` is optional and should be blank when no external standard code exists.
3. `Status` typically uses `active` or `inactive`.

Persistence:

- report-local copy: execution snapshot for the current run
- durable promotion target: `{userDatastore}/data/knowledge/themes/ThemeRegistry.csv`

### `ThemeMap.csv`

Per-symbol primary theme assignment.

Schema:

```text
Symbol,ThemeId,MappingConfidence,PrimaryFlag,Notes
```

Rules:

1. Use one primary theme row per symbol for current report rollups.
2. Additional non-primary rows are allowed only if a future capability explicitly supports multi-theme appendices.
3. Symbols may be omitted when `rollupLens: standards`.

Persistence:

- report-local copy: execution snapshot for the current run
- durable promotion target: `{userDatastore}/data/knowledge/themes/ThemeMapCurrent.csv` and `ThemeMapHistory.csv`

### `ThesisRegistry.csv`

Catalog of active and historical portfolio theses.

Schema:

```text
ThesisId,ThesisStatement,ParentThemeId,HorizonStart,HorizonEnd,PrimaryCatalyst,Status,Notes
```

Canonical `Status` values:

- `active`
- `watch`
- `closed`
- `invalidated`

Persistence:

- report-local copy: execution snapshot for the current run
- durable promotion target: `{userDatastore}/data/knowledge/theses/ThesisRegistry.csv`

### `ThesisAssignment.csv`

Per-symbol primary thesis assignment for thesis-lens reporting.

Schema:

```text
Symbol,ThesisId,AssignmentConfidence,PrimaryFlag,Notes
```

Rules:

1. Use one primary thesis row per symbol for current report rollups.
2. Symbols may remain unassigned when they are residual holdings, pure liquidity, or intentionally outside active thesis coverage.
3. Residual symbols should still appear in `HoldingsMap.csv`.

Persistence:

- report-local copy: execution snapshot for the current run
- durable promotion target: `{userDatastore}/data/knowledge/theses/ThesisAssignmentCurrent.csv` and `ThesisAssignmentHistory.csv`

### `MappingDiscovery.md`

Unified working copy for user confirmation during Input Discovery.

Contents:

1. holdings map confirmation transcript
2. theme map confirmation transcript when `rollupLens` is `theme` or `thesis`
3. thesis registry confirmation transcript when `rollupLens` is `thesis`

The operative content must be embedded in `Report.md` Appendix A.

## Capability responsibilities

### `holdings-standards-map`

Creates `HoldingsMap.csv` for the full mapping universe.

### `theme-map-inference`

Creates `ThemeRegistry.csv` and `ThemeMap.csv` when `rollupLens` is `theme` or `thesis`.

### `thesis-registry-inference`

Creates `ThesisRegistry.csv` and `ThesisAssignment.csv` when `rollupLens` is `thesis`.

### Confirmation capabilities

- `holdings-map-confirmation`
- `theme-map-confirmation`
- `thesis-registry-confirmation`

These are additive, not mutually exclusive.

## Input Discovery gates

Aggregate state review must not proceed to quantification until the required mapping gates for the chosen lens are complete.

### Always required

```text
[ ] Holdings Map Confirmed
```

### Required when `rollupLens: theme`

```text
[ ] Theme Map Confirmed
```

### Required when `rollupLens: thesis`

```text
[ ] Theme Map Confirmed
[ ] Thesis Registry Confirmed
```

## Mapping universe

When a playbook computes period evolution, rotation, or symbol-level flows, the mapping universe is the union of:

1. period-start holdings
2. period-end holdings
3. reference snapshot holdings
4. all symbols with filled orders in the analysis period

Normalize tickers before mapping. Do not allow unmapped symbols to roll silently into a catch-all group when the symbol can be classified.

## Reporting rules

### Standards lens

Primary weights table:

```text
Sector / Liquidity | Period Start % | Period End % | Delta pp
```

Appendices should include:

- complete `HoldingsMap` summary
- `AssetClass` exposure table
- `StyleBucket` exposure table

### Theme lens

Primary weights table:

```text
Theme / Residual Bucket / Liquidity | Period Start % | Period End % | Delta pp
```

Appendices should include:

- standards-based holdings summary
- complete `ThemeMap`

### Thesis lens

Primary weights table:

```text
Thesis / Liquidity | Period Start % | Period End % | Delta pp
```

Appendices should include:

- parent theme grouping
- standards-based holdings summary
- complete thesis registry and assignment summaries

## Cross-playbook enrichment

`HoldingsMap.csv` is reusable across playbooks:

- `aggregate-state-review` uses it directly
- `environment-review` may use it to choose market proxies for owned sectors and asset classes
- `activity-period-review` may use it to tag activity by sector, theme, or thesis when supplied
- `unit-decision-review` may use it to add sector, theme, or thesis context for the target symbol

`ThemeMap.csv` and `ThesisAssignment.csv` are optional enrichments outside aggregate-state-review.

## Non-goals

This taxonomy does not attempt to:

- preserve legacy `CategoryMap.csv` or `ThesisMap.csv` semantics
- keep a binary `thematic` abstraction
- force every security into an active thesis
- replace user judgment for liquidity intent or thesis definition

## Migration stance

Historical report folders remain archival evidence and should not be retrofitted.

New development should target:

- `HoldingsMap.csv`
- `ThemeRegistry.csv`
- `ThemeMap.csv`
- `ThesisRegistry.csv`
- `ThesisAssignment.csv`
- `MappingDiscovery.md`

If a legacy artifact name appears elsewhere in the repository, treat it as technical debt to be retired rather than a compatibility target.
