# TeamFoundry Stack Realignment Plan

This document tracks planning status for the TeamFoundry stack realignment. It follows the roadmap pillars from `teamfoundry-stack-realignment-vision.md` and is intended to evolve from high-level objectives into bounded planning notes, decisions, and next actions.

Program bootstrap and read order live in `README.md`.

## Current Focus

**Phase:** Baseline Pillar 1 and prepare the first pilot.

**Now:**

- Use `app-design.md` as the current APP shared behavior contract baseline.
- Use `tfy-design.md` as the current TeamFoundry ingestion, translation, and simulator baseline.
- Keep `teamfoundry.ai` read-only while APP concepts and simulator design stabilize.
- Do not edit the TFY repo or build production adapter code yet.

**Next:**

- Choose one pilot behavior from the candidate list in Pillar 7.
- Create the first TFY-derived APP example under `examples/`.
- Stub or implement the local simulator under `tools/tfy-simulator/`.
- Run one end-to-end preview through ingest, resolve, assemble, translate, and report.

**Not Yet:**

- TFY repo integration or importer implementation
- Production OpenClaw adapter implementation
- Broad APP schema changes without pilot pressure
- Rewriting the vision document

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

- Refine `app-design.md` based on the first pilot behavior.
- Identify which contract elements the first pilot requires beyond the current baseline.
- Align manifest draft fields in `schema/app-manifest-v0.1.md` only when the pilot exposes a real gap.

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

**Status:** Not Started

**Objective:** Separate foundational TeamFoundry constructs such as TeamFoundry Employee into identity, reusable behavior, runtime activation, and operational governance units.

**Planning Notes:**

- TBD

**Decisions:**

- TBD

**Next Actions:**

- TBD

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

- Baseline translation and simulator sections in `tfy-design.md`.
- Baseline consumption profile expectations in `app-design.md`.
- Stub `tools/tfy-simulator/` and run one pilot preview through the full TFY-mediated path.

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

**Status:** Not Started

**Objective:** Select one concrete TeamFoundry behavior to test whether APP can represent reusable assistant behavior and whether TeamFoundry can translate it into an engine-specific assistant instance.

**Candidate Pilots:**

- TeamFoundry Employee base behavior
- Warren or another investment-advisor assistant behavior
- Portfolio analysis or market report behavior
- HQ request intake behavior

**Planning Notes:**

- TBD

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
