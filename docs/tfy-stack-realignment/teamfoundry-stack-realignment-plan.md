# TeamFoundry Stack Realignment Plan

This document tracks planning status for the TeamFoundry stack realignment. It follows the roadmap pillars from `teamfoundry-stack-realignment-vision.md` and is intended to evolve from high-level objectives into bounded planning notes, decisions, and next actions.

Program bootstrap and read order live in `README.md`.

## Current Focus

**Phase:** Pillar 1 POC — TradingCoach APP prototype.

**Process:** Iterate the prototype in the repo. Do not update this plan, design docs, or decision logs during exploratory POC work. When the POC is complete, update pillar 1 here with design lessons learned.

**Active work:** See **POC** under pillar 1 below.

**Deferred:** `sketches/teamfoundry-employee-base/` and `tools/tfy-simulator/` until after the Pillar 1 POC.

## Pilot Materialization Status

**APP distribution repo (workbench):** `examples/` — `README.md` + `trading-coach.app/` only.

**TradingCoach:** Full legacy translation materialized (5 playbooks, 23 skills, 3 workflows, 6 overlays, contracts, gates). Regenerate with `tools/migrate-trading-coach.py` (read-only source: `C:\code\trading-coach`).

**Deferred pilot sketch:** `sketches/teamfoundry-employee-base/`

## Working Assumptions

All workstations used for this plan should keep the APP and TeamFoundry repositories as side-by-side clones in the same parent folder. OpenClaw may also be cloned adjacent when engine-specific details need confirmation. For example:

```text
C:\code\agent-playbook-pack
C:\code\teamfoundry.ai
C:\code\openclaw
```

Development agents should treat `agent-playbook-pack` as the active planning workspace and `teamfoundry.ai` as the adjacent reference project for TeamFoundry concepts, examples, and migration candidates. Use `openclaw` as an optional reference repo for runtime-native mechanics, not as a source-of-truth behavior format. This is a temporary working-context assumption, not a permanent repo coupling, monorepo structure, or submodule relationship.

## Highest-Level Work Patterns

### Two-Step TFY Implementation Pattern

**Status:** Exploring

**Intent:** Keep TeamFoundry stable while APP concepts are still changing by treating the TeamFoundry repo as a read-only reference first, then applying validated APP concepts back into TeamFoundry later through a deliberate integration path.

**Step 1: Read TFY, Build APP**

During early realignment work, development agents should read from `teamfoundry.ai` but should not edit it. TFY acts as the source corpus for real assistant behavior, including skills, casts, habits, forged examples, request workflows, and operational patterns. APP remains the active implementation workspace where those behaviors are translated into packs, playbooks, examples, schemas, and adapter concepts.

**Step 2: Validate With A Local TFY Simulator**

APP development should use a local TFY simulator or translation harness to test whether APP content can plausibly become TeamFoundry assistant construction input. The simulator should not attempt to become TeamFoundry or OpenClaw. It should exercise the translation boundary and produce preview artifacts such as assistant construction plans, engine-specific inventory previews, dependency warnings, and translation manifests.

**Later Integration Back To TFY**

Only after APP representations stabilize should TFY receive implementation changes. At that point, TFY can add docs, importers, adapters, or migration logic that consumes APP packs as assistant behavior input while preserving TFY's ownership of assistant storefront, curation, deployment, operations, and governance.

**Expected Outputs:**

- APP examples derived from real TeamFoundry behavior
- A local TFY simulator or translation harness in the APP workspace
- Translation preview artifacts that show how APP content would map to TFY or OpenClaw-shaped outputs
- Integration-readiness notes before any TFY repo changes
- Later TFY adapter or importer work after the APP contract is credible

**Guardrails:**

- Do not use early APP exploration as a reason to mutate the TFY repo.
- Do not let the simulator become the runtime engine.
- Do not treat OpenClaw-shaped outputs as the APP source of truth.
- Do not create permanent repo coupling, submodules, or monorepo assumptions.
- Do use TFY examples to pressure-test APP against real assistant behavior.

### Source-Of-Truth Boundaries

The source-of-truth boundary model is defined in `teamfoundry-stack-realignment-vision.md`. This plan document should reference that model rather than duplicate it. Planning notes should use those boundaries when deciding whether work belongs in APP, TeamFoundry, Agent Skills, OpenClaw, another agent engine, or the local simulator.

### Pilot-First Translation Pattern

**Status:** Exploring

**Intent:** Use one concrete TeamFoundry behavior at a time to test APP's behavior-pack model before generalizing schemas, adapters, or migration plans.

**Pattern:**

1. Select one bounded TeamFoundry behavior from the read-only reference repo.
2. Translate that behavior into APP pack, playbook, skill, workflow, overlay, contract, or example concepts.
3. Validate the translation with the local TFY simulator or translation harness.
4. Record what the pilot exposed about APP expressiveness, TFY ownership boundaries, engine adapter needs, and unresolved decisions.
5. Generalize only after the pilot has produced a useful translation result.

**Candidate Inputs:**

- TeamFoundry Employee base behavior
- Warren or another investment-advisor assistant behavior
- Portfolio analysis or market report behavior
- HQ request intake behavior

**Guardrails:**

- Do not broaden the APP schema from theory alone when a pilot can pressure-test the idea.
- Do not migrate multiple TFY behaviors at once until the translation shape is credible.
- Do not treat simulator success as TFY integration completion.
- Do preserve notes about what remains TFY-owned, APP-owned, skill-owned, or engine-owned.

### Design Decision Log Pattern

**Status:** Exploring

**Intent:** Preserve important architecture and product-design choices as durable planning notes before they become hidden implementation assumptions.

**Pattern:**

When a pillar produces a meaningful **design** decision, record a short row in the **APP Design Decision Log** or **TFY Design Decision Log** table below (or in that pillar's `Decisions` section until promoted). Use the table columns: Date, Status, Decision, Impact. Keep rows brief; expand in design docs when needed.

Do not record program coordination, documentation process, or pilot selection here. Those belong in **Current Focus**, work patterns, or pillar planning notes.

**Guardrails:**

- Do not rely on chat history as the only record of design decisions.
- Do not over-document transient ideas that have not affected direction.
- Do record decisions that change source-of-truth boundaries, schema shape, translation model, adapter assumptions, or ownership of behavior concepts.
- Do not use this log for status tracking, README scope, vision-doc editing rules, or which pilot is active.

### Adapter-Last Pattern

**Status:** Exploring

**Intent:** Keep APP focused on behavior intent before introducing runtime-specific adapter mechanics.

**Pattern:**

1. Express the selected behavior in APP terms first.
2. Validate that the APP representation is understandable without a specific engine.
3. Use the local simulator to expose the translation gap.
4. Define OpenClaw or other engine adapter details only after the gap is visible.
5. Feed adapter lessons back into APP concepts only when they reveal a general framework need.

**Guardrails:**

- Do not let OpenClaw inventory shape become the APP source format.
- Do not build adapter mechanics before the behavior contract is clear.
- Do not ignore runtime constraints; capture them as adapter requirements or compatibility notes.
- Do preserve APP runtime neutrality while using OpenClaw as the first concrete adapter target.

### Sketch-Then-Materialize Pattern

**Status:** Accepted

**Intent:** Separate design exploration from durable example files so agents do not assume sketched files already exist.

**Pattern:**

1. Capture the full pilot proposal in the example README when helpful.
2. Materialize only the minimum files needed for the next validation step.
3. Record materialization status in this plan document under **Pilot Materialization Status**.
4. Add one playbook, skill, or contract file at a time after each validation step.

**Guardrails:**

- Do not create an entire example tree from a sketch in one step unless explicitly requested.
- Do not treat README manifest blocks as proof that files exist on disk.
- Do not use README files to track materialization or program status.
- Do update **Pilot Materialization Status** in this plan when files are added.

### Schema Precedent Pattern

**Status:** Accepted

**Intent:** Allow pilots to introduce manifest fields without prematurely generalizing the APP schema.

**Pattern:**

1. Pilot examples may use provisional manifest fields.
2. Record **Accepted** rows in the APP Design Decision Log only after a pilot validates a field or pattern.
3. Update `schema/app-manifest-v0.1.md` and `app-design.md` only after acceptance.

**Guardrails:**

- Do not copy pilot-only fields into global schema without acceptance.
- Do not reject pilot fields solely because the baseline schema lacks them yet.

### Agent Handoff Pattern

**Status:** Accepted

**Intent:** Let the repo stand on its own when a Cursor thread ends.

**Pattern:**

1. Use `AGENTS.md` and `docs/tfy-stack-realignment/README.md` as entry points.
2. Use this plan document for status, immediate priorities, and pilot materialization state.
3. Use the APP and TFY design decision log tables for accepted design direction.
4. Do not rely on chat history as program state.

**Guardrails:**

- Do not leave pilot selection, schema choices, or file existence implicit in conversation only.
- Do not track program status in README files.
- Do update this plan before ending a major thread when status or decisions changed.

### README Scope Pattern

**Status:** Accepted

**Intent:** Keep README files stable and infrequently updated. Program status belongs in the plan document only.

**Pattern:**

1. Folder READMEs explain how to use a directory: read order, document roles, reference maps, artifact locations.
2. Example READMEs explain pack intent, source corpus, design sketches, and boundary tables.
3. Status, current phase, materialization progress, next actions, and decisions live in the plan document.
4. Verify file existence on disk or in **Pilot Materialization Status** before assuming an example file exists.

**Guardrails:**

- Do not add status tables, current phase sections, or next-action lists to README files.
- Do not duplicate plan content in README files.
- Do update the plan when status changes.

### Current-State Design Documentation Pattern

**Status:** Exploring

**Intent:** Keep design documentation useful as a clean statement of the current design model, while using the vision document and APP/TFY design decision logs for different purposes.

**Documentation Layers:**

- Vision document: baseline strategic intent; stable after acceptance.
- Plan document: active work tracking, pillar status, work patterns, and design decisions.
- Design documents: complete current design thinking for a specific concept.
- Implementation artifacts: examples, schemas, simulator code, adapters, and migration outputs.

**Pattern:**

Create or update a design document when a concept becomes too detailed for this plan document but is not yet ready to graduate into durable framework docs or schema docs. Design documents should represent the current best understanding of how the concept works, what it owns, what it excludes, and which implementation surfaces it affects.

**Guardrails:**

- Do not rewrite the vision document to track later pivots; treat it as the baseline thesis once accepted.
- Do not use design documents to narrate history, editorial commentary, or past discarded models.
- Do not duplicate the design decision logs inside design documents.
- Do keep design documents current, direct, and complete enough for implementation agents to act from.
- Do record meaningful design pivots in the APP or TFY design decision log, then update the relevant design document so it reflects the accepted current design.
- Do graduate stable design content into framework docs, schema docs, examples, or adapter docs when it becomes durable.
- Do keep this plan document monolithic for shared coordination, while keeping product design in separate design documents.
- Do separate APP design and TeamFoundry design so development agents do not mix source-of-truth boundaries.

**Design Documents:**

- `app-design.md`: APP as the portable behavior contract.
- `tfy-design.md`: TeamFoundry assistant construction, storefront, operations, APP consumption, translation, and simulator model.

## Design Decision Log

Record **accepted** product and architecture design decisions here by primary ownership. Only `Accepted` rows belong in these tables; open questions resolve in POC work or graduate here when accepted.

Do not use this section for program process (status tracking, README rules, pilot selection, or documentation layout). Those live in **Current Focus**, accepted work patterns, and pillar planning notes.

### APP Design Decision Log

| Date | Status | Decision | Impact |
| --- | --- | --- | --- |
| 2026-06-21 | Accepted | APP repo holds **behavior only**: no user datastore contents, run archives, or broker data committed as part of normal pack operation. Local APP install is a read-only working copy of published behavior. | Separates behavior contract from user state; replaces git-as-live-workspace model. |
| 2026-06-21 | Accepted | All persistent and working paths use **logical roles** (`userDatastore`, `agentWorkspace`) in contracts, skills, and output templates—not repo-relative paths or engine adapters like `trading-coach/reports`. | Executing agent binds roles from pack-level inputs at runtime. |
| 2026-06-21 | Accepted | APP packs are **user-agnostic**; user-specific history, inputs, and saved reports live only in the bound user datastore. | Replaces single-user product-repo conflation. |
| 2026-06-21 | Accepted | Granular procedures use **Agent Skills** (`skills/<name>/SKILL.md`); ASP `capabilities/` + `capabilityKind` are not an APP standard. | Migration converts capabilities to skills; APP manifests reference skills only. |
| 2026-06-21 | Accepted | **`pack.app.yaml` is the primary manifest**; playbooks use `playbook.app.yaml`. Retire `.asp.yaml`, per-artifact `productId`, and scattered product identity. | Centralizes pack identity, inputs, paths, and playbook index. |
| 2026-06-21 | Accepted | **Framework docs live in `agent-playbook-pack`**; domain packs ship as `{packId}.app/` instances in APP distribution repos, not as framework hosts. | Replaces `AgenticSkillPackREADME.md` co-located in product repo. |
| 2026-06-21 | Accepted | **Git is not an APP execution requirement.** Version control may back a user datastore if the user chooses; APP does not require commit-on-run, inventory files, or git transactions. | Decouples execution from git workflow. |
| 2026-06-21 | Accepted | **Manifest-first bootstrap**: `pack.app.yaml` + minimal pack README + referenced manifests/contracts are sufficient entry; large execution constitutions decompose into `workflows/`, `gates/`, and `contracts/`. | Replaces multi-doc read chain (`PROJECT.md`, git protocol, etc.) as mandatory bootstrap. |
| 2026-06-21 | Accepted | **No engine-specific wiring in APP repos** (e.g. `.cursor/rules`, engine-named adapters in manifests). Consumer platforms own runtime integration. | Keeps APP runtime-neutral; integration lives in TFY/Cursor/OpenClaw consumer. |
| 2026-06-21 | Accepted | **Durable rules live under `contracts/`**; playbooks and skills reference contract files by path. Root-level ad hoc contract docs are not the APP pattern. | Consolidates `DATASTORE_CONTRACT.md`, report rules, taxonomy, etc. into `contracts/`. |
| 2026-06-21 | Accepted | **Prompt-first execution with optional workspace artifacts**: default path is skill procedures in markdown; agent workspace may hold intermediate files and ephemeral scripts; durable outputs go to user datastore. | Supersedes strict no-script-during-runs rule where workspace intermediates are needed. |
| 2026-06-21 | Accepted | **Structured run manifest** (YAML/JSON per APP schema) is the canonical run record; human-readable `Manifest.md` in report folders is an optional derivative. | Enables reference executor and programmatic consumption. |
| 2026-06-21 | Accepted | **Playbook-scoped overlays are allowed** (`layer3-playbooks/<id>/overlays/`); legacy `treatments/` redirect layer is dropped; canonical playbook ids from legacy (e.g. `aggregate-state-review`) are preserved. | Aligns overlay placement with APP while keeping legacy intent names. |
| 2026-06-21 | Accepted | Execution uses two data locations arbitrated by the executing agent: **agent workspace** (agent-controlled temp/intermediate artifacts) and **user datastore** (user-controlled persistent APP data). Neither belongs in the APP repo. | Fixes TradingCoach-style conflation of persistent data with repo contents; contracts reference logical roles, not repo paths. |
| 2026-06-21 | Accepted | High-level APP dependencies (including datastore and workspace bindings) are declared as **pack-level inputs** in top-level APP metadata (`pack.app.yaml`). | Executing agent resolves concrete paths/locations before playbook execution; playbook inputs remain workflow-specific. |
| 2026-06-21 | Accepted | APP repos are public distribution units; client agent platforms pull read-only copies on their own schedule into a local APP install (no live repo tracking or dev-time coupling). | Consumers own update cadence and local layout; APP repo is the authoritative published source. |
| 2026-06-21 | Accepted | An APP repo must be self-sufficient: repo `README.md` indexes `*.app/` packs; each instance provides bootstrapping context for pack discovery and playbook use. | Instance layout and entry guidance must not depend on external TFY or consumer-specific docs for routine operation. |
| 2026-06-21 | Accepted | Playbook inputs may declare `resolveFrom` referencing **pack-level input ids** or named logical roles (e.g. `userDatastore`). Consumer-specific assembly paths are not APP manifest vocabulary. | Executing agent or consumer adapter binds values; TFY deployment context stays outside APP. |
| 2026-06-21 | Accepted | Skills describe **engine-neutral scope and intent** (categories, artifact shapes, procedures)—not concrete paths, scripts, or engine inventory locations. | Adapters and executing agents map scope to runtime surfaces; aligns with logical-role data locations. |
| 2026-06-21 | Accepted | Pack implementation folders use **layer-prefixed names**: `layer0-workflows/`, `layer1-skills/`, `layer2-overlays/`, `layer3-playbooks/`. Cross-cutting `contracts/` and `gates/` stay unprefixed at pack root. Playbook-scoped overlays live under `layer3-playbooks/<id>/overlays/`. | `pack.app.yaml` `paths` block declares roots; sort order matches framework layers 0–3. |
| 2026-06-21 | Accepted | Each APP instance is **self-contained** in `{packId}.app/` (e.g. `trading-coach.app/`). All pack behavior, layer folders, and `pack.app.yaml` live inside that directory. | Consumers address one folder per pack; supports multi-pack APP repos. |
| 2026-06-21 | Accepted | **`layer1-skills/` holds referenced skills in agentskills.io format** (`<skill-name>/SKILL.md`, optional `references/`, `scripts/`, `assets/`). | APP composes skills; does not redefine skill packaging. |
| 2026-06-21 | Accepted | **APP distribution repos** contain only `README.md` (pack index) and one or more `*.app/` instance folders at repo root—no other top-level files. | Clean pull target for client platforms; repo README indexes available packs. |
| 2026-06-21 | Accepted | **Execution interface** is three inputs: APP repo address, execution directive (target pack and playbook), and optional partial input params. The executing agent mediates all missing pack-level, playbook-level, and infrastructure bindings during the run. | No multi-doc bootstrap or consumer-specific wiring required at invoke time; aligns with manifest-first packs and input-discovery workflows. |
| 2026-06-21 | Accepted | Each APP instance **owns its user datastore layout** via pack contracts (e.g. `contracts/user-datastore-layout.md`); TradingCoach preserves legacy `data/` and `reports/` structure under `{userDatastore}/`. | Pack-specific persistence conventions stay with the pack, not the framework. |
| 2026-06-21 | Accepted | Workbench path `examples/` models an APP distribution repo root (`README.md` + `*.app/` only) for the TradingCoach POC. | Aligns execution interface testing with published repo shape. |

| 2026-06-21 | Accepted | **Canonical instance layout is convention, not manifest.** Only `pack.app.yaml` and `playbook.app.yaml` are APP manifests; layer folders, contracts, gates, and workflows use markdown only; skills use `SKILL.md`. Omit `paths:` and playbook paths when using standard layout. | Executors resolve fixed folder names; playbook index is id list only. |
| 2026-06-21 | Accepted | **`docs/app-execution.md`** is the framework execution-agent guide; each `{packId}.app/` instance includes **`APP-EXECUTION.md`** so pulled APP repos are self-sufficient without the workbench. | Separates runtime instructions from `app-design.md` development design. |

### TFY Design Decision Log

| Date | Status | Decision | Impact |
| --- | --- | --- | --- |
| 2026-06-21 | Accepted | Identity, persona, and deployment-context preconditions (e.g. `identity-context-loaded`) are **TFY assembly scope**, not APP pack gates. | APP gates cover behavior-contract preconditions only; TFY resolves identity before playbook execution. |
| 2026-06-21 | Accepted | Pack `consumptionProfile` (composition role, compose order, required assembly context) is **TFY consumer metadata** for Forge/HQ ingestion—not core APP schema. | APP stays runtime-neutral; TFY ingestion layer owns composition metadata. |
| 2026-06-20 | Accepted | Translation is TFY-owned via assistant assembly; OpenClaw is first adapter target. | Design in `tfy-design.md`; APP stays runtime-neutral. |

## Status Legend

- `Not Started`: No substantive planning work has begun.
- `Exploring`: Concepts are being investigated or compared.
- `Drafting`: A proposed direction is being written down.
- `Ready For Pilot`: The pillar is clear enough to test with a concrete example.
- `Validated`: A pilot or review has confirmed the direction.
- `Deferred`: Intentionally postponed.

## 1. APP As The Shared Behavior Contract

**Status:** Drafting

**Objective:** Define APP as the neutral behavior contract between granular Agent Skills and assistant systems.

**POC:**

Baseline pillar 1 by completing a rapid but complete TradingCoach APP prototype in this repo:

1. ~~Translate the TradingCoach legacy project into a materialized `trading-coach.app/` instance~~ **Done** — `examples/trading-coach.app/` (regenerate: `tools/migrate-trading-coach.py`).
2. Build a reference execution implementation in this repo (not the TFY simulator) that can drive a playbook end-to-end.
3. Point an existing TFY agent at the repo and execute one TradingCoach playbook as the initial consumption pilot.

**Planning Notes:**

- Current baseline lives in `app-design.md`.
- General APP framework references remain in `docs/framework.md`, `docs/agent-skills-integration.md`, and `schema/app-manifest-v0.1.md` until design content graduates.
- Capture design lessons learned in this pillar after POC completion; defer schema promotion and decision-log updates until then.

**Decisions:**

- See **APP Design Decision Log** (updates deferred until POC completion).

**Next Actions:**

- Complete the POC above. Update this pillar with outcomes when done.

## 2. TFY Skills Migration To APP-Compatible Skills

**Status:** Not Started

**Objective:** Migrate, mirror, or normalize TeamFoundry skills toward APP-compatible Agent Skills shape.

**Planning Notes:**

- TBD

**Decisions:**

- TBD

**Next Actions:**

- TBD

## 3. Base Persona And Employee Behavior Realignment

**Status:** Deferred

**Objective:** Separate foundational TeamFoundry constructs such as TeamFoundry Employee into identity, reusable behavior, runtime activation, and operational governance units.

**Planning Notes:**

- Deferred until after Pillar 1 POC.
- Working sketch: `sketches/teamfoundry-employee-base/README.md`.

**Decisions:**

- TBD

**Next Actions:**

- TBD

## 4. APP-To-Engine Translation Layer

**Status:** Drafting

**Objective:** Define how APP behavior intent becomes engine-native artifacts through TeamFoundry ingestion, assistant assembly, and target engine translation, with OpenClaw as the first adapter target.

**Planning Notes:**

- The baseline vision pillar name remains APP-to-engine, but the accepted current model is TFY-mediated translation. See **TFY Design Decision Log** (translation row).
- Primary translation design lives in `tfy-design.md`, including APP ingestion, assistant assembly, HQ-deployable output, simulator model, and OpenClaw adapter preview.
- APP-side translation inputs live in `app-design.md`, especially adapter profile expectations and what APP must expose for TeamFoundry consumption.
- Do not treat direct APP-to-runtime mappings as the implementation model unless a pilot proves a narrower path is sufficient.

**Decisions:**

- See **TFY Design Decision Log** (translation row).

**Next Actions:**

- Deferred until after Pillar 1 POC.

## 5. TFY Assistant Construction Model

**Status:** Not Started

**Objective:** Reframe TeamFoundry assistant construction around modular inputs such as identity, persona, knowledge, APP packs, Agent Skills, habits, policies, memories, customer context, engine profile, and deployment target.

**Planning Notes:**

- TBD

**Decisions:**

- TBD

**Next Actions:**

- TBD

## 6. Pack Store Versus TFY Storefront Boundary

**Status:** Not Started

**Objective:** Clarify the boundary between reusable APP behavior distribution and TeamFoundry's human-facing assistant storefront.

**Planning Notes:**

- TBD

**Decisions:**

- TBD

**Next Actions:**

- TBD

## 7. Pilot Migration

**Status:** Deferred

**Objective:** Select one concrete TeamFoundry behavior to test whether APP can represent reusable assistant behavior and whether TeamFoundry can translate it into an engine-specific assistant instance.

**Planning Notes:**

- Initial consumption pilot is folded into Pillar 1 POC (TradingCoach playbook execution via existing TFY agent).
- TFY employee-base migration deferred; sketch at `sketches/teamfoundry-employee-base/`.

**Decisions:**

- TBD

**Next Actions:**

- TBD

## 8. Wind-Down Of Multi-Repo Mode

**Status:** Not Started

**Objective:** Define exit criteria for ending the temporary side-by-side multi-repo working mode.

**Planning Notes:**

- TBD

**Decisions:**

- TBD

**Next Actions:**

- TBD
