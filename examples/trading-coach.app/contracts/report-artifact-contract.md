# Reports

Generated TradingCoach reports. **New** folders sort chronologically by execution time (timestamp-first).

## Canonical Generated Report Pattern (ASP — new reports)

```text
{userDatastore}/reports/<GenerationTimestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>/
```

| Token | Format |
|---|---|
| `GenerationTimestamp` | `YYYYMMDD-HHMMSS` (first — wall-clock at folder creation) |
| `PlaybookReportId` | PascalCase playbook id |
| `AnalysisStart` / `AnalysisEnd` | `YYYYMMDD` (last two tokens — analysis period range) |

| Playbook | PlaybookReportId |
|---|---|
| Aggregate State Review | `AggregateStateReview` |
| Environment Review | `EnvironmentReview` |
| Unit Decision Review | `UnitDecisionReview` |
| Activity Period Review | `ActivityPeriodReview` |
| Source Profile | `SourceProfile` |

Example:

```text
{userDatastore}/reports/20260619-172303-AggregateStateReview-20260501-20260531/
```

### Timestamp rules

- Use **actual** generation time (`date +%Y%m%d-%H%M%S` or equivalent) — no placeholders.
- **Never overwrite** an existing folder; create a new timestamp if the path exists.

### Legacy pattern (historical only)

```text
{userDatastore}/reports/<AnalysisStart>-<AnalysisEnd>-<PlaybookReportId>-<GenerationTimestamp>/
```

Do not use for new reports.

## Manifest ASP fields

`Manifest.md` for new reports should include:

```text
Product Id: trading-coach
Playbook Id: <playbook-id>
Playbook Report Id: <PlaybookReportId>
Asp Schema Version: 1.0
Playbook Version: <semver>
Generation Timestamp: <YYYYMMDD-HHMMSS>
Canonical Report Name: <GenerationTimestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>
Output Folder: {userDatastore}/reports/<Canonical Report Name>/
Output Mode: core | augmented
Capabilities Executed: <id> (<capabilityKind>), ...
Workflows Executed: ...
Overlays Executed: <id> (<overlayKind>), ...
Lenses Resolved: ...
Evaluation: true | false
```

## Preferred Report Artifacts

```text
Manifest.md
Report.md
Report.pdf
<Canonical Report Name>.pdf
Interview.md
ExitInterview.md
InputSummary.md
MarketResearch.md
Metrics.csv
```

## Self-Contained Reports

`Report.md` must stand on its own for human review. See **Report Self-Containment Contract** in `../PROJECT.md`.

## Historical Reports

Prior reports are immutable. Historical folders may use legacy period-first names or deprecated treatment ids. **New** reports use timestamp-first PlaybookReportId naming.

## Git version control

Report folders are **fully tracked in git**. Every artifact in a report folder belongs in the repository:

- markdown (`Report.md`, interviews, summaries)
- CSV tables (metrics, exposure, maps, rotation matrices)
- PDFs (`Report.pdf`, distribution copies)
- `SourceData/` exports copied for run evidence

On report finalization, agents must stage and commit the **complete** report folder as part of the repository transaction (see `../AGENT_GIT_PROTOCOL.md`).

Do not add `{userDatastore}/reports/` to `.gitignore`.

**Execution-local** (in `contracts/persistent-knowledge-model.md`) means an artifact is not auto-promoted into `{userDatastore}/data/knowledge/`. It does **not** mean excluded from git.
