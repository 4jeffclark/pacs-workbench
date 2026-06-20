# TeamFoundry Stack Realignment Plan

This document tracks planning status for the TeamFoundry stack realignment. It follows the roadmap pillars from `teamfoundry-stack-realignment-vision.md` and is intended to evolve from high-level objectives into bounded planning notes, decisions, and next actions.

Program bootstrap and read order live in `README.md`.

## Current Focus

**Phase:** First pilot materialization and simulator validation.

**Accepted pilot:** `examples/teamfoundry-employee-base/` derived from TFY `teamfoundry-employee` cast v1.0.5.

**Now:**

- Treat `examples/teamfoundry-employee-base/` as the active pilot example.
- Use only pilot files listed under **Pilot Materialization Status** below unless a task explicitly adds more.
- Keep `teamfoundry.ai` read-only.
- Extend simulator design in `tfy-design.md`; implement automated simulator only when a bounded task is assigned.

**Next:**

- Materialize `contracts/backup-artifact-contract.md` for the accepted pilot.
- Re-run or refresh the hand preview after new pilot files land.
- Record Accepted schema decisions only after pilot pressure justifies them.

**Not Yet:**

- TFY repo integration or importer implementation
- Production OpenClaw adapter implementation
- Broad APP schema changes without pilot pressure
- Rewriting the vision document

## Pilot Materialization Status

Track example and preview file status here, not in README files.

**Accepted pilot:** `examples/teamfoundry-employee-base/`

| Path | Status |
| --- | --- |
| `pack.app.yaml` | Materialized |
| `playbooks/daily-backup/playbook.app.yaml` | Materialized |
| `skills/backup-to-hq-zip/SKILL.md` | Materialized |
| Other playbooks, skills, workflows, contracts, overlays | Sketch only in example README |

**Simulator preview:**

| Path | Status |
| --- | --- |
| `tools/tfy-simulator/input/daily-backup-preview.yaml` | Hand-authored input spec |
| `tools/tfy-simulator/output/` | Hand-authored preview artifacts |
| Automated simulator implementation | Not started |

**Suggested next materialization:** `contracts/backup-artifact-contract.md`

Do not assume pilot files exist unless listed as materialized above or verified on disk.

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

### Decision Log Pattern

**Status:** Exploring

**Intent:** Preserve important architecture choices as durable planning notes before they become hidden implementation assumptions.

**Pattern:**

When a pillar produces a meaningful decision, record a short entry in that pillar's `Decisions` section or move it later into a dedicated decision log. Each entry should capture:

- Context: what question or tension prompted the decision
- Decision: what direction was chosen
- Rationale: why this direction is preferred now
- Impact: which repos, examples, schemas, adapters, or migration paths are affected

**Guardrails:**

- Do not rely on chat history as the only record of architecture decisions.
- Do not over-document transient ideas that have not affected direction.
- Do record decisions that change source-of-truth boundaries, pilot scope, adapter assumptions, or repo responsibilities.

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
2. Log new field ideas as **Proposed** decisions until a pilot validates them.
3. Promote fields to **Accepted** only when the pilot exposes a real gap that the baseline schema cannot express.
4. Update `schema/app-manifest-v0.1.md` and `app-design.md` only after acceptance.

**Guardrails:**

- Do not copy pilot-only fields into global schema without acceptance.
- Do not reject pilot fields solely because the baseline schema lacks them yet.

### Agent Handoff Pattern

**Status:** Accepted

**Intent:** Let the repo stand on its own when a Cursor thread ends.

**Pattern:**

1. Use `AGENTS.md` and `docs/tfy-stack-realignment/README.md` as entry points.
2. Use this plan document for status, immediate priorities, and pilot materialization state.
3. Use the decision log for accepted direction.
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

**Intent:** Keep design documentation useful as a clean statement of the current design model, while using the vision document and decision log for different purposes.

**Documentation Layers:**

- Vision document: baseline strategic intent; stable after acceptance.
- Plan document: active work tracking, pillar status, work patterns, and decisions.
- Design documents: complete current design thinking for a specific concept.
- Implementation artifacts: examples, schemas, simulator code, adapters, and migration outputs.

**Pattern:**

Create or update a design document when a concept becomes too detailed for this plan document but is not yet ready to graduate into durable framework docs or schema docs. Design documents should represent the current best understanding of how the concept works, what it owns, what it excludes, and which implementation surfaces it affects.

**Guardrails:**

- Do not rewrite the vision document to track later pivots; treat it as the baseline thesis once accepted.
- Do not use design documents to narrate history, editorial commentary, or past discarded models.
- Do not duplicate the decision log inside design documents.
- Do keep design documents current, direct, and complete enough for implementation agents to act from.
- Do record meaningful pivots in the decision log, then update the relevant design document so it reflects the accepted current design.
- Do graduate stable design content into framework docs, schema docs, examples, or adapter docs when it becomes durable.
- Do keep this plan document monolithic for shared coordination, while keeping product design in separate design documents.
- Do separate APP design and TeamFoundry design so development agents do not mix source-of-truth boundaries.

**Design Documents:**

- `app-design.md`: APP as the portable behavior contract.
- `tfy-design.md`: TeamFoundry assistant construction, storefront, operations, APP consumption, translation, and simulator model.

## Decision Log

Use this section for architecture decisions that affect realignment direction, source-of-truth boundaries, pilot scope, adapter assumptions, or repo responsibilities.

### Decision Entry Template

**Date:** YYYY-MM-DD

**Status:** Proposed | Accepted | Superseded

**Context:** TBD

**Decision:** TBD

**Rationale:** TBD

**Impact:** TBD

### 2026-06-20: TFY-Mediated Translation Model

**Status:** Accepted

**Context:** The baseline vision describes an APP-to-engine translation layer with direct illustrative mappings from APP concepts to runtime artifacts. Subsequent design work clarified that TeamFoundry should ingest APP packs as a native assistant-construction input layer and translate assembled assistant context into HQ-deployable, engine-specific artifacts.

**Decision:** Translation is TeamFoundry-owned through assistant assembly context. APP expresses portable behavior intent and adapter-facing expectations. TeamFoundry ingests APP packs, assembles assistant inputs, and runs the translation path to target engine deployables. Engine adapters operate at the end of that path, with OpenClaw as the first concrete target.

**Rationale:** This preserves APP runtime neutrality, keeps TeamFoundry as the assistant construction and operations layer, and avoids treating OpenClaw-shaped inventory as the long-term source format for reusable behavior.

**Impact:** Primary translation design lives in `tfy-design.md`. APP adapter profile expectations live in `app-design.md`. Pillar 4 planning should follow this split rather than treating translation as a direct APP-to-engine concern. The vision document remains the unchanged baseline thesis.

### 2026-06-20: Documentation And Design Track Model

**Status:** Accepted

**Context:** Realignment work spans APP and TeamFoundry design evolution, but the two products must remain architecturally separable for development agents.

**Decision:** Keep one monolithic plan document with a shared decision log. Maintain two current-state design documents: `app-design.md` for APP and `tfy-design.md` for TeamFoundry including translation and simulator design. Do not use a separate translation design document or a mixed design index.

**Rationale:** Coordination is shared, but source-of-truth boundaries differ. Separate design documents reduce agent context mixing while preserving one program plan.

**Impact:** All future design updates must target the correct design document. The plan remains the shared coordination surface.

### 2026-06-20: Vision Document Immutability

**Status:** Accepted

**Context:** The vision document defines the baseline thesis, but later design work may refine implementation details such as TFY-mediated translation.

**Decision:** Treat `teamfoundry-stack-realignment-vision.md` as the accepted baseline vision. Do not rewrite it to track later pivots. Record pivots in the decision log and update the relevant current-state design document instead.

**Rationale:** Preserve a stable strategic anchor while allowing design to evolve based on pilots and implementation learning.

**Impact:** When vision language conflicts with accepted design, follow the plan decision log and current design documents.

### 2026-06-20: First Pilot Selection

**Status:** Accepted

**Context:** The program needed one bounded TFY behavior to test APP expressiveness and TFY-mediated translation boundaries.

**Decision:** Use `teamfoundry-employee-base` as the first pilot, derived from TFY cast `teamfoundry-employee` v1.0.5. Initial materialization focuses on the `daily-backup` playbook.

**Rationale:** TeamFoundry Employee is mandatory on every forged assistant, mixes portable operating behavior with clearly TFY-owned identity and deployment content, and exposes scheduled-behavior translation without requiring a full TFY migration.

**Impact:** Active example lives at `examples/teamfoundry-employee-base/`. Pillars 1, 3, 4, and 7 should reference this pilot. Other candidate pilots remain deferred.

### 2026-06-20: Playbook Schedule Metadata

**Status:** Proposed

**Context:** The `daily-backup` pilot needs to express scheduled behavior intent before TFY translates it to engine-native cron/habit artifacts.

**Decision:** Allow `schedule` on playbook manifests during the pilot.

**Rationale:** Scheduled behavior is part of portable workflow intent and should not be encoded only as OpenClaw habit JSON in APP.

**Impact:** Do not generalize into `schema/app-manifest-v0.1.md` until the pilot preview validates the shape.

### 2026-06-20: Input resolveFrom References

**Status:** Proposed

**Context:** Some playbook inputs depend on TFY assembly context such as deployment channels and supervisor targets.

**Decision:** Allow playbook inputs to declare `resolveFrom` references to assembly context rather than embedding deployment values in APP.

**Rationale:** Preserves APP runtime neutrality while making TFY assembly requirements explicit.

**Impact:** Document in pilot example and `app-design.md` if accepted after simulator validation.

### 2026-06-20: Pack consumptionProfile Metadata

**Status:** Proposed

**Context:** TeamFoundry base packs need to express composition role and required assembly context.

**Decision:** Allow pack-level `compatibility.consumptionProfile` metadata during the pilot.

**Rationale:** Helps TFY ingest APP packs as assistant construction input without turning APP into a persona or deployment system.

**Impact:** Do not generalize into global schema until validated by simulator preview and Forge composition review.

### 2026-06-20: identity-context-loaded Gate Placement

**Status:** Proposed

**Context:** Session readiness requires identity context, but identity content is TFY-owned.

**Decision:** Undecided whether `identity-context-loaded` belongs in APP gates or only as a TFY assembly precondition outside the pack.

**Rationale:** This affects how strictly APP can declare prerequisites without owning identity content.

**Impact:** Resolve during `session-readiness` materialization or simulator preview; do not treat as accepted APP schema yet.

### 2026-06-20: Skill Backup Scope Categories

**Status:** Proposed

**Context:** Materializing `backup-to-hq-zip/SKILL.md` required separating portable backup intent from TFY/OpenClaw-specific paths in the source skill.

**Decision:** APP skills may describe backup and restore scope as engine-neutral **categories** (configuration state vs content state). Concrete paths, exec scripts, and storage locations are adapter or TFY assembly concerns.

**Rationale:** Preserves runtime neutrality while keeping enough procedure detail for translation planning. Matches the pilot boundary that APP references behavior, not deployment paths.

**Impact:** Future engine adapters map categories to inventory paths. May inform `app-design.md` skill authoring guidance if accepted after next simulator preview.

### 2026-06-20: Retention Policy In Skill Vs Contract

**Status:** Proposed

**Context:** The TFY source skill embeds retention tiers inline. The pilot sketch also places retention rules in `contracts/backup-artifact-contract.md`.

**Decision:** Undecided whether retention tiers should live only in the output contract, only in the skill procedure, or in both with the contract as canonical for outputs.

**Rationale:** Duplication risks drift; skill-only retention may be insufficient for playbook output validation without a materialized contract.

**Impact:** Resolve when materializing `contracts/backup-artifact-contract.md` or re-running simulator resolve for `daily-backup`.

### 2026-06-20: README Scope For Program Docs

**Status:** Accepted

**Context:** Status tracking began appearing in folder and example README files, duplicating the plan and increasing maintenance churn.

**Decision:** README files in this program explain how to use a folder or example. All status updates, materialization progress, current phase, and next actions belong in `teamfoundry-stack-realignment-plan.md` only.

**Rationale:** Keeps READMEs stable and infrequently updated while preserving one coordination surface for agents.

**Impact:** Update **Pilot Materialization Status** and **Current Focus** in this plan. Do not add status sections to README files.

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

**Planning Notes:**

- Current baseline lives in `app-design.md`.
- The shared behavior contract includes pack identity, playbook intent, inputs, skill references, workflows, gates, overlays, contracts, outputs, run manifest, and consumption profile expectations.
- General APP framework references remain in `docs/framework.md`, `docs/agent-skills-integration.md`, and `schema/app-manifest-v0.1.md` until design content graduates.
- APP must be complete enough for TeamFoundry to ingest without requiring TFY persona or deployment context inside the pack definition.

**Decisions:**

- See decision log entries dated 2026-06-20.

**Next Actions:**

- Validate which pilot fields beyond the current baseline are required for `daily-backup`.
- Promote Proposed schema decisions to Accepted only after simulator preview.

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

**Status:** Drafting

**Objective:** Separate foundational TeamFoundry constructs such as TeamFoundry Employee into identity, reusable behavior, runtime activation, and operational governance units.

**Planning Notes:**

- Active pilot: `examples/teamfoundry-employee-base/`.
- APP owns portable operating workflows such as backup, routing, signing, and session readiness intent.
- TFY owns identity placeholders, handbook, memories, deployment config, and runtime activation artifacts.
- See the pilot README boundary table as the working artifact for this pillar.

**Decisions:**

- See decision log entry: 2026-06-20 First Pilot Selection.

**Next Actions:**

- Use the pilot boundary table to refine what remains TFY-owned during materialization.
- Defer role-specific cast behavior to later pilots or separate APP packs.

## 4. APP-To-Engine Translation Layer

**Status:** Drafting

**Objective:** Define how APP behavior intent becomes engine-native artifacts through TeamFoundry ingestion, assistant assembly, and target engine translation, with OpenClaw as the first adapter target.

**Planning Notes:**

- The baseline vision pillar name remains APP-to-engine, but the accepted current model is TFY-mediated translation. See the 2026-06-20 decision log entry.
- Primary translation design lives in `tfy-design.md`, including APP ingestion, assistant assembly, HQ-deployable output, simulator model, and OpenClaw adapter preview.
- APP-side translation inputs live in `app-design.md`, especially adapter profile expectations and what APP must expose for TeamFoundry consumption.
- Do not treat direct APP-to-runtime mappings as the implementation model unless a pilot proves a narrower path is sufficient.

**Decisions:**

- See decision log entry: 2026-06-20 TFY-Mediated Translation Model.

**Next Actions:**

- Produce simulator input spec for `examples/teamfoundry-employee-base/pack.app.yaml` and `playbooks/daily-backup/playbook.app.yaml`.
- Run one preview through ingest, resolve, assemble, translate, and report.

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

**Status:** Ready For Pilot

**Objective:** Select one concrete TeamFoundry behavior to test whether APP can represent reusable assistant behavior and whether TeamFoundry can translate it into an engine-specific assistant instance.

**Accepted Pilot:**

- `examples/teamfoundry-employee-base/` from TFY `teamfoundry-employee` cast v1.0.5

**Deferred Candidates:**

- Warren or another investment-advisor assistant behavior
- Portfolio analysis or market report behavior
- HQ request intake behavior

**Planning Notes:**

- Full pilot design sketch lives in `examples/teamfoundry-employee-base/README.md`.
- Materialization and simulator preview status live in **Pilot Materialization Status**.
- Hypothesis remains partially validated; self-contained APP preview still blocked by missing contracts and skills.

**Decisions:**

- See decision log entry: 2026-06-20 First Pilot Selection.

**Next Actions:**

- Materialize `contracts/backup-artifact-contract.md`.
- Refresh hand preview after new pilot files land.
- Materialize the next pilot unit only after reviewing preview results.

## 8. Wind-Down Of Multi-Repo Mode

**Status:** Not Started

**Objective:** Define exit criteria for ending the temporary side-by-side multi-repo working mode.

**Planning Notes:**

- TBD

**Decisions:**

- TBD

**Next Actions:**

- TBD
