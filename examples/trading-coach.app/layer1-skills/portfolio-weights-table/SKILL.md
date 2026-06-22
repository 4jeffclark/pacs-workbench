---
name: portfolio-weights-table
description: TradingCoach skill: portfolio-weights-table
sourceCorpus:
  repository: trading-coach
  path: capabilities/portfolio-weights-table/
  readOnly: true
metadata:
  legacyCapabilityKind: synthesize
---

Requires completed `period-weight-reconstruction` and confirmed maps.

Period header in report:

```text
Period Start: YYYY-MM-DD | Period End: YYYY-MM-DD
Thematic Analysis: true | false
Weight methods: start=<source> end=<source>
```

**Primary table — Section 3:**

| When `thematic: true` | When `thematic: false` |
|---|---|
| Column: **Theme / Bucket** | Column: **Category** |
| Rows: each thesis + generic bucket + `Liquidity` | Rows: each category + `Liquidity` |

| … | Period Start % | Period End % | Δ pp |

Populate `ThesisExposure.csv` or `CategoryExposure.csv` and `GenericBucketExposure.csv` with weight source columns.

Embed complete exposure tables in `Report.md` Appendix F (or treatment-specified appendix) — sibling CSVs are duplicates for tooling.

**Figure 1 — Portfolio Composition pie** using **period-end weights**; title includes period-end date.

Pie rules: denominator = total live account value at period end; liquidity slice = total liquidity %; combine slices <1% into `Other` only when needed.

**GitHub rendering:** use `pie showData` only (see **Report.md Rendering Conventions** in `PROJECT.md`). **Disallowed:** `xychart-beta` and other non-GitHub chart types.

**Required:** duplicate Figure 1 data as a markdown table in Section 3 (the table is canonical; the pie is optional visual).

Optional **Figure 2** (top categories bar-style view): use a markdown table only — do not use Mermaid bar/xy charts.

## Outputs

- Report Section 3 table and Figure 1
- `ThesisExposure.csv` / `CategoryExposure.csv`, `GenericBucketExposure.csv`

## Used by

- `layer3-playbooks/aggregate-state-review`