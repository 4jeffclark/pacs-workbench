# TradingCoach

`trading-coach.app/` is an [AgentPlaybookPack](https://github.com/4jeffclark/agent-playbook-pack) (APP) instance as defined at [github.com/4jeffclark/agent-playbook-pack](https://github.com/4jeffclark/agent-playbook-pack.git).

Migrated from legacy TradingCoach (ASP v3.1). Persistent data and reports belong under the bound `userDatastore` (see `contracts/user-datastore-layout.md`), not in this behavior repo.

## Playbooks

| Playbook id | Report id | Path |
| --- | --- | --- |
| `aggregate-state-review` | `AggregateStateReview` | [layer3-playbooks/aggregate-state-review/](layer3-playbooks/aggregate-state-review/) |
| `environment-review` | `EnvironmentReview` | [layer3-playbooks/environment-review/](layer3-playbooks/environment-review/) |
| `unit-decision-review` | `UnitDecisionReview` | [layer3-playbooks/unit-decision-review/](layer3-playbooks/unit-decision-review/) |
| `activity-period-review` | `ActivityPeriodReview` | [layer3-playbooks/activity-period-review/](layer3-playbooks/activity-period-review/) |
| `source-profile` | `SourceProfile` | [layer3-playbooks/source-profile/](layer3-playbooks/source-profile/) |

## Execution

Invoke via APP execution interface: repo address, directive (`pack: trading-coach`, `playbook: <id>`), and optional partial `inputs`. See [`APP-EXECUTION.md`](APP-EXECUTION.md).

---

## Legacy Product README (reference)

# TradingCoach

Structured trading performance reviews and debriefs.

Repository: [github.com/4jeffclark/trading-coach](https://github.com/4jeffclark/trading-coach)

TradingCoach is an **AgenticSkillPack (ASP)** for investment and active-trading analysis, evaluation, and coaching. For framework concepts—pack layout, composition, manifests, agent layer—see **[AgenticSkillPackREADME.md](AgenticSkillPackREADME.md)**.

The pack is **prompt-first**: playbooks and contracts live in markdown. Any capable agent that can read this repository and write artifacts here can run an analysis. E*TRADE CSV exports are the first supported data source; the persistent datastore under `data/` merges raw exports into normalized canonical tables so analyses can span months or years without re-uploading history every session.

---

## What you can ask for

TradingCoach helps answer five kinds of questions. Each maps to a **playbook**—a user intent, not a CLI command.

| User intent | Playbook | Typical question |
|---|---|---|
| **Portfolio** | Aggregate state review | What do I hold, how did it change, and is the construction sound? |
| **Market** | Environment review | What regime am I trading in, and how does it affect my book? |
| **Trade** | Unit decision review | Was this entry, exit, stale hold, or event trade sound? |
| **Trading** | Activity period review | How did my day or week of trading perform? |
| **Data** | Source profile | What data do I have, and is it fit for analysis? |

**Quantification** produces metrics, inventories, and factual context—no coaching or verdict. **Evaluation** adds structured interviews, scorecards, judgments, and exit debriefs. Say what you want in natural language; the agent resolves parameters during input discovery.

Example requests:

- *Review my portfolio for May—metrics only, no coaching.*
- *How is my book positioned for a risk-off market?*
- *Post-mortem on my IPO allocation last month.*
- *Profile the datastore—I want to know what date range I can analyze.*

---

## Playbooks

### Portfolio — aggregate state review

*What is my book, how did it change over the period, and optionally—is the construction sound?*

**Lenses** (inferred from your request, confirmed during input discovery):

| Lens | Default | Effect |
|---|---|---|
| `evaluation` | coaching on | Metrics-only vs full evaluation |
| `rollupLens` | `theme` | `standards` = GICS-first, `theme` = structural themes, `thesis` = active hypotheses |
| `compositionReview` | on | Holdings, theme, thesis, and liquidity mapping plus weights |
| `rebalancingReview` | off | Reshaping quality, concentration, redeployment |
| `riskReview` | off | Risk posture, de-risking, cash-raising behavior |

One playbook replaces what were separate portfolio, thematic, rebalancing, and risk treatments. Lenses combine orthogonally.

**Key behaviors:**

- Period boundary **weight reconstruction** from holdings snapshots and order flow when exports bracket the analysis window
- **Primary weights table** (start % → end %) as the central quantification artifact
- **HoldingsMap** standards classification plus optional theme and thesis layers; order-flow symbols mapped to a declared universe
- Cash and cash-equivalents (treasuries, TIPs, money market) as a first-class liquidity slice
- Optional embedded market summary; full market depth routes to the Market playbook

**Entry point:** `layer3-playbooks/aggregate-state-review/playbook.md` (legacy: `treatments/PortfolioAnalysis.md`)

### Market — environment review

*What market regime applies, and how does it interact with my positions or thesis?*

Standalone memo or embedded summary inside a portfolio report. Portfolio runs may embed light market context or reference a full environment review when depth is requested.

**Entry point:** `layer3-playbooks/environment-review/playbook.md`

### Trade — unit decision review

*Was this specific trade or position decision sound?*

Consolidates position lifecycle, stale-position hygiene, and event-driven trades (IPO, secondary, etc.) with focus parameters:

- `reviewFocus`: lifecycle · stale · event
- `eventType`: optional qualifier for event-driven reviews

**Entry point:** `layer3-playbooks/unit-decision-review/playbook.md` (legacy: `treatments/PositionLifecycle.md`, `StalePositionReview.md`, `IPOTrading.md`)

### Trading — activity period review

*How did my trading activity over a day or week perform?*

Day-trading and short-horizon debriefs: execution patterns, P&L attribution, behavioral signals.

**Entry point:** `layer3-playbooks/activity-period-review/playbook.md` (legacy: `treatments/DayTrading.md`)

### Data — source profile

*What data exists, over what range, and is it analysis-ready?*

Datastore inventory and quality assessment. No entry interview; quantification-only by default.

**Entry point:** `layer3-playbooks/source-profile/playbook.md` (legacy: `treatments/DataStoreProfile.md`)

---

## Running an analysis

Attach broker export CSVs when adding new data. The agent:

1. Follows `contracts/datastore-contract.md` to merge non-duplicate files into `{userDatastore}/data/raw/etrade/` and rebuild `{userDatastore}/data/canonical/`
2. Selects the playbook from your request
3. Runs **input discovery**—resolves lenses, presents **Inputs Resolved**, confirms analysis period
4. Conducts entry and exit interviews when `evaluation` is true (except data profile)
5. Writes a timestamped report folder under `{userDatastore}/reports/`

Every **execution run** starts with the **TradingCoach Framework** handshake (product, playbook, version, phase, gates). Catalog or discovery questions do not require a handshake. See `AGENTS.md` and `PROJECT.md` for the canonical format.

Reports are **immutable** after finalization and **fully version-controlled in git** (markdown, CSV, PDF, `SourceData/`). Each folder includes at minimum `Report.md` (self-contained) and `Manifest.md` (run metadata).

### Report folder naming (ASP-native)

New reports use **PlaybookReportId** in folder names—not legacy treatment ids:

```text
{userDatastore}/reports/<GenerationTimestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>/
```

Use actual wall-clock time for `GenerationTimestamp` (`YYYYMMDD-HHMMSS`). Never overwrite an existing report folder.

| Playbook | PlaybookReportId |
|---|---|
| Aggregate state review | `AggregateStateReview` |
| Environment review | `EnvironmentReview` |
| Unit decision review | `UnitDecisionReview` |
| Activity period review | `ActivityPeriodReview` |
| Source profile | `SourceProfile` |

Historical reports retain their original ids (for example `ThematicPortfolioAnalysis`) and are never renamed.

---

## Data

| Path | Role |
|---|---|
| `{userDatastore}/data/raw/etrade/` | Immutable broker export archive |
| `{userDatastore}/data/canonical/` | Normalized tables rebuilt from all raw files |
| `contracts/datastore-contract.md` | Merge rules, deduplication keys, validation |

---

## Repository layout

```text
layer3-playbooks/      User-intent workflows (Layer 3)
layer1-skills/   Reusable expert work units (Layer 1)
layer0-workflows/      Infrastructure modules (Layer 0)
schema/         ASP manifest schema and examples
treatments/     Legacy stubs (deprecated; route to layer3-playbooks/)
data/           Persistent E*TRADE datastore
{userDatastore}/reports/        Generated analyses (immutable, fully git-tracked)
reference/      Supporting notes; archived POC material
```

See [AgenticSkillPackREADME.md](AgenticSkillPackREADME.md) for framework layout conventions.

---

## Legacy treatment names

Prior reports and invocations used **treatment** ids. These route to playbooks and lenses:

| Legacy treatment | Routes to |
|---|---|
| `ThematicPortfolioAnalysis`, `ThematicRotation` | Portfolio playbook, `rollupLens: theme` |
| `PortfolioRebalancing` | Portfolio playbook, `rebalancingReview: true` |
| `RiskRotation` | Portfolio playbook, `riskReview: true` |
| `PositionLifecycle`, `StalePositionReview`, `IPOTrading` | Trade playbook (planned consolidation) |

Historical report folders keep their original treatment ids and are not renamed.

Deprecated alias files:

- `treatments/ThematicPortfolioAnalysis.md`
- `treatments/ThematicRotation.md`

---

## Start here

| Role | Read first |
|---|---|
| **Browsing / what's available** | [README.md](README.md) → [layer3-playbooks/README.md](layer3-playbooks/README.md) |
| **Running an analysis** | [PROJECT.md](PROJECT.md) → [AGENT_GIT_PROTOCOL.md](AGENT_GIT_PROTOCOL.md) → [contracts/datastore-contract.md](contracts/datastore-contract.md) → playbook under `layer3-playbooks/` |
| **Extending the pack** | [DEVELOPMENT.md](DEVELOPMENT.md) → [AGENTS.md](AGENTS.md) → [PROJECT.md](PROJECT.md) |
| **Agent-layer bootstrap** | [docs/agent-bootstrap.md](docs/agent-bootstrap.md) → [docs/agent-layer-integration.md](docs/agent-layer-integration.md) |
| **ASP framework** | [AgenticSkillPackREADME.md](AgenticSkillPackREADME.md) |
| **Repository inventory** | [REPO_INVENTORY.md](REPO_INVENTORY.md) |

Use `REPO_INVENTORY.md` and direct file paths for discovery. Do not rely solely on GitHub code search.

Archived ChatGPT connector POC material lives under `reference/archives/` and is not part of the default reading path.

---

## Status

TradingCoach is an **AgenticSkillPack** product (Framework v3.1). ASP layout is complete: `layer3-playbooks/`, `layer1-skills/`, `layer0-workflows/`, `schema/`. Legacy `treatments/` stubs route to playbooks. New reports use PlaybookReportIds.

This README is the **TradingCoach product specification**. Framework specification lives in [AgenticSkillPackREADME.md](AgenticSkillPackREADME.md).
