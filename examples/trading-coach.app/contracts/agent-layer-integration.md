# Agent Layer Integration

Required ASP pack document per [AgenticSkillPackREADME.md](../AgenticSkillPackREADME.md) — translator and platform reference implementation guide for consuming this pack. Engine-native routing graphs and MCP servers may live in a separate agent-layer project; this file is the pack-owned contract they implement.

## Product identity

| Field | Value |
|---|---|
| Product id | `trading-coach` |
| Repository | https://github.com/4jeffclark/trading-coach |
| ASP schema version | `1.0` |
| Framework version | `3.1` |

## Agent bootstrap

All platforms should implement the three-mode routing in [agent-bootstrap.md](agent-bootstrap.md):

| Mode | Trigger | Read path |
|---|---|---|
| Discovery | Catalog / capability questions | `README.md` → `layer3-playbooks/README.md` |
| Execution | Run intent expressed | `PROJECT.md` → `AGENT_GIT_PROTOCOL.md` → `contracts/datastore-contract.md` → playbook |
| Factory | Extend pack or contracts | `DEVELOPMENT.md` → `AGENTS.md` → `PROJECT.md` |

## Read order for translators

1. [AgenticSkillPackREADME.md](../AgenticSkillPackREADME.md) — framework
2. [README.md](../README.md) — product playbooks
3. [schema/asp-manifest-v1.md](../schema/asp-manifest-v1.md) — manifest schema
4. [PROJECT.md](../PROJECT.md) — execution constitution
5. `layer3-playbooks/<id>/playbook.md` — playbook specs
6. `layer3-playbooks/<id>/*.asp.yaml` — machine-readable composition

## Playbook index

| Playbook id | Path | Report id |
|---|---|---|
| `aggregate-state-review` | `layer3-playbooks/aggregate-state-review/` | `AggregateStateReview` |
| `environment-review` | `layer3-playbooks/environment-review/` | `EnvironmentReview` |
| `unit-decision-review` | `layer3-playbooks/unit-decision-review/` | `UnitDecisionReview` |
| `activity-period-review` | `layer3-playbooks/activity-period-review/` | `ActivityPeriodReview` |
| `source-profile` | `layer3-playbooks/source-profile/` | `SourceProfile` |

## Translator expectations

- Map natural-language user intent → playbook id + lens parameters
- Support discovery turns without forcing a handshake or datastore reads
- Emit **TradingCoach Framework** handshake only after run intent is clear
- Resolve inputs via **Structured Inputs Framework**; present **Inputs Resolved**
- Write report folders using **timestamp-first** naming (`{userDatastore}/reports/<GenerationTimestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>/`)
- Populate `Manifest.md` with ASP execution record fields (`Output Mode`, typed layer1-skills/overlays)
- Finalize `Report.md` self-contained per `PROJECT.md` (full Appendix C citations; GitHub-safe Mermaid + table fallbacks; report narrative is agent-authored — data scripts may write intermediate CSVs only)
- Do not require users to type CLI-style parameter syntax

## Layer paths

```text
layer0-workflows/     Layer 0 — context, inputs, scope, gates
layer1-skills/  Layer 1 — retrieve, transform, synthesize, analyze, plan, interact, validate
layer3-playbooks/*/overlays/  Layer 2 — optional augmentations (evaluation, advisory, enrichment, …)
layer3-playbooks/     Layer 3 — user intents
```

See [AgenticSkillPackREADME.md](../AgenticSkillPackREADME.md) for capability and overlay kinds.

## Platform reference implementations

Baseline patterns for two agent engines. Each mirrors [agent-bootstrap.md](agent-bootstrap.md) with engine-native wiring.

### Cursor

**Status:** Reference implementation ships in this repository.

Cursor simulates an arm's-length agent layer when the user opens a **fresh chat** with the workspace open. Persistent bootstrap comes from project rules (`.cursor/rules/`), not from conversation history.

#### Files in this repo

| File | Role |
|---|---|
| [docs/agent-bootstrap.md](agent-bootstrap.md) | Platform-neutral bootstrap (discovery / execution / factory) |
| `.cursor/rules/asp-consumer.mdc` | Always-on consumer routing — catalog and execution |
| `.cursor/rules/asp-factory.mdc` | File-scoped factory routing when editing pack artifacts |

#### Consumer rule behavior (`asp-consumer.mdc`)

- `alwaysApply: true` — every chat gets pack-consumer defaults
- **Discovery:** read `README.md` and `layer3-playbooks/README.md`; no handshake, no datastore
- **Execution:** after run intent, read constitution + selected playbook; emit handshake per `AGENTS.md`
- **Avoid by default:** `DEVELOPMENT.md`, `docs/asp-validation-suite.md`, `reference/archives/`

#### Factory rule behavior (`asp-factory.mdc`)

- `alwaysApply: false`; activates on globs under `layer3-playbooks/`, `layer1-skills/`, `layer0-workflows/`, `schema/`, `treatments/`, and contract docs
- Points agents at `DEVELOPMENT.md` before durable pack changes
- Keeps agent-layer docs aligned when bootstrap changes

#### Simulating arm's-length use

1. Commit and sync the repo so the agent sees current playbooks and manifests.
2. Open a **new chat** (empty context).
3. Start free-form: *"What playbooks can you run?"* or *"Review my portfolio for May — metrics only."*
4. Do not `@`-mention validation docs, refactor plans, or prior reports unless testing regression.

The consumer rule is intentionally minimal. Deeper execution detail lives in pack-owned docs (`AGENTS.md`, `PROJECT.md`), not in Cursor config.

**Report finalization:** enforce self-contained `Report.md`, GitHub-safe Mermaid + table fallbacks — see **Report finalization** in `.cursor/rules/asp-consumer.mdc`. Bundled skill scripts under `layer1-skills/*/scripts/` per agentskills.io are allowed when `SKILL.md` instructs.

#### What stays out of Cursor config

- Full handshake template (in `AGENTS.md` / `PROJECT.md`)
- Playbook procedures (in `layer3-playbooks/` and `layer1-skills/`)
- Cursor Skills for execution — optional elsewhere; not required for this reference

---

### OpenClaw

**Status:** Baseline spec only — engine wiring lives in the OpenClaw agent-layer project, not in TradingCoach.

OpenClaw typically separates **pack content** (this repo) from **routing and tooling** (translator graph, skills, MCP servers). Mirror the same three-mode bootstrap.

#### Recommended workspace layout

```text
<openclaw-workspace>/
  trading-coach/          # git clone or submodule — ASP pack (this repo)
  skills/                 # optional OpenClaw-native skill wrappers
  routing/                # intent → playbook mapping graph
  mcp/                    # file, git, web research servers
```

#### Bootstrap mapping

| agent-bootstrap mode | OpenClaw responsibility |
|---|---|
| Discovery | Router reads `README.md` + `layer3-playbooks/README.md`; responds without invoking execution subgraph |
| Execution | Router selects playbook id + lenses → loads `playbook.md` + `.asp.yaml` → runs Layer 0 workflows then layer1-skills/overlays |
| Factory | Separate dev skill or graph branch; reads `DEVELOPMENT.md` first |

#### Suggested skill / graph responsibilities

1. **Catalog skill** — answers "what can you do?" from product README; no git writes.
2. **Intent router** — NL → `{ playbookId, lenses }`; confirms ambiguous lenses in one reconciliation turn.
3. **Execution subgraph** — handshake → datastore merge → input discovery → capability chain → report folder write → optional PDF hook.
4. **Git transaction skill** — implements `AGENT_GIT_PROTOCOL.md` (stage, commit message style, no force-push).

#### MCP expectations

| Server | Use |
|---|---|
| Filesystem | Read pack; write under `{userDatastore}/reports/` and `{userDatastore}/data/raw/` per contract |
| Git | Status, diff, commit when user requests |
| Web | Market research for `market-environment` capability |

#### Handshake and manifest

Same pack contracts as Cursor: emit TradingCoach Framework block after run intent; write `Manifest.md` with `Output Mode`, `Capabilities Executed` with `capabilityKind`, and `Overlays Executed` with `overlayKind`.

#### OpenClaw-specific out of scope (in TradingCoach repo)

- OpenClaw skill YAML / graph definitions
- MCP server implementations
- Session memory or cross-run state beyond the git-backed datastore

When OpenClaw wiring stabilizes, copy proven patterns back into this section or link to the external agent-layer repo.

## Out of scope for this repo

Engine-specific routing graphs and MCP server **implementations** belong in the agent-layer project. **Cursor reference rules** and **platform baseline docs** in this file are the exception — they document how to consume the pack, not replace pack content.
