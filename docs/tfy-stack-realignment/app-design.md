# APP Design

## Purpose

This document captures the current design model for APP as the portable behavior contract in the TeamFoundry stack realignment.

APP design should describe what APP owns as a framework: packs, playbooks, skill references, gates, overlays, contracts, outputs, run manifests, compatibility metadata, examples, and consumption-facing expectations for TeamFoundry and other pack consumers.

Baseline strategic intent lives in `teamfoundry-stack-realignment-vision.md`. Active planning, status, work patterns, and decisions live in `teamfoundry-stack-realignment-plan.md`.

## Related Design Documents

- `tfy-design.md`: TeamFoundry assistant construction, storefront, operations, APP consumption, translation, and simulator model.

## Documentation Rules

- Keep this design document current-state only.
- Do not narrate design history in this document.
- Do not duplicate the design decision log in this document.
- Record meaningful design pivots in `teamfoundry-stack-realignment-plan.md`.
- Update this document after a decision so it reflects the accepted current APP design.
- Graduate stable APP design into `docs/framework.md`, `schema/`, `examples/`, or adapter docs when it becomes durable.

## Framework References

During realignment, use these as the general APP framework references:

- `docs/framework.md`
- `docs/agent-skills-integration.md`
- `docs/naming.md`
- `schema/app-manifest-v0.1.md`
- `examples/trading-coach.app/`

This document defines the current realignment-specific behavior contract model and may evolve ahead of those files during pilots.

## Status

Drafting

## Current Design Summary

APP is the shared behavior contract between granular Agent Skills and assistant systems such as TeamFoundry.

An APP pack describes reusable assistant behavior and domain workflows in a runtime-neutral way. It defines what should happen for a user intent, which skills and workflows are involved, which gates must clear, which overlays may apply, and which outputs and run records should result.

APP does not deploy assistants, operate storefronts, assemble persona context, or emit engine-native deployable artifacts directly. Those responsibilities belong to TeamFoundry and target agent engines through the translation path described in `tfy-design.md`.

## APP Repository And Consumption Model

An APP is distributed as a **public repository** that client agent platforms consume by maintaining a **local copy** of the repo contents.

### APP Distribution Repo Layout

An APP distribution repo has **only** these top-level entries:

```text
README.md              # index of packs in this repo
trading-coach.app/     # self-contained APP instance
other-pack.app/        # additional instances when present
```

No other files or folders belong at the repo root. The repo `README.md` indexes each `*.app/` pack (name, intent, version pointer).

During POC, `agent-playbook-pack/examples/` models this distribution repo shape. The framework workbench (`docs/`, `schema/`, `tools/`) lives outside that root.

### APP Instance Layout

Each pack is a **self-contained** `{packId}.app/` directory. All behavior contract files live inside the instance folder. See **Pack Layout And Naming** below.

### Pull Model

- Client platforms **pull read-only** from the published APP repo when they choose to update.
- Consumers control **update cadence** on their own schedule.
- Consumers do **not** track the APP repo directly for normal operation — no live sync, submodule coupling, or dev-time dependency on APP source control state.
- The local copy is the working surface for discovery, invocation, and execution.

### Self-Sufficient Bootstrap

The APP distribution repo must provide **all bootstrapping context required for normal use**. A consumer should be able to install or refresh a local copy, read the repo `README.md` pack index, enter a `{packId}.app/` folder, and operate that pack without external documentation.

Minimum bootstrap surface **per instance** (`{packId}.app/`):

- `pack.app.yaml` — identity, pack-level inputs, `paths` roots, playbook index
- instance `README.md` — domain intent and how to invoke playbooks
- referenced playbooks, skills, workflows, gates, overlays, and contracts

Large monolithic execution constitutions (legacy `PROJECT.md` style) decompose into workflows, gates, and contracts—not a mandatory multi-document read chain before execution.

At minimum, each instance should make discoverable:

- pack and playbook manifests
- local skills in `layer1-skills/` (agentskills.io format), workflows, overlays, contracts, and gates referenced by those manifests
- enough entry guidance for an agent or runtime to find packs, resolve playbooks, and begin execution

Consumer platforms provide runtime integration (Cursor rules, TFY assembly, OpenClaw inventory). Those do not ship inside the APP repo.

Persistent APP data and agent working files are **not** part of the repo. See **Execution Data Locations** below.

## Execution Interface

Invoking an APP run should require only:

1. **APP repo address** — local path or pulled copy of an APP distribution repo (`README.md` + `*.app/`). Used for pack index, instance manifests, skills, workflows, contracts, and pack documentation.
2. **Execution directive** — which pack to run and what to execute (playbook id, natural-language intent, or equivalent selector resolved to a playbook).
3. **Optional input params** — partial map of known pack-level and playbook-level values. Omitted keys are **not** errors at invoke time.

The **executing agent** mediates everything not supplied in step 3, including:

- `agentWorkspace` location (temp and intermediate artifacts)
- `userDatastore` location (persistent APP data)
- remaining pack-level inputs declared in `pack.app.yaml`
- remaining playbook-level inputs declared in `playbook.app.yaml`
- app and playbook options discovered through workflows (e.g. input discovery, period confirmation)

Reference implementations and framework documentation may live in a separate workbench repo during development (e.g. `agent-playbook-pack`). They are not required at the APP distribution repo root. Client platforms embed or pair an executor with the APP repo address.

Example invoke shape (conceptual):

```yaml
appRepo: /local/copy/of/trading-coach-repo   # or git URL before pull
directive:
  pack: trading-coach                        # resolves to trading-coach.app/
  playbook: aggregate-state-review           # or intent: "review my portfolio for May"
inputs:                                      # all optional
  userDatastore: ~/TradingCoachData
  playbook:
    evaluation: false
```

### Ownership Boundary

| Concern | Owner |
| --- | --- |
| Published behavior contract and repo contents | APP repo |
| When to pull and where the local copy lives | Client agent platform |
| User datastore location and persistent APP data | User (bound by executing agent) |
| Agent workspace location and ephemeral execution artifacts | Executing agent |
| Runtime secrets, persona, and deployment context | Client agent platform |
| Translation to engine-native deployables | Consumer adapter (e.g. TeamFoundry) when applicable |

## Execution Data Locations

APP behavior produces and consumes data, but **datastores do not live in the APP repo**. The executing agent arbitrates two distinct locations:

### Agent Workspace

Controlled by the executing agent. Used for:

- temporary files and scratch data
- intermediate data products during a run
- optional ephemeral scripts or one-off helpers when needed
- other artifacts that need not survive across sessions

**Prompt-first** remains the default execution style: agents follow skill and workflow procedures in markdown. Workspace artifacts supplement that path; they are not a substitute for durable contracts.

The APP repo may ship behavior definitions and templates; it does not own workspace contents.

### User Datastore

Controlled by the user. Used for:

- persistent APP data that survives across runs and sessions
- historical inputs, outputs, and domain records the APP expects over time
- durable artifacts named by contracts (reports, snapshots, run history, etc.)
- structured run manifests for completed executions

TradingCoach-style holdings, period inputs, and saved reports belong here—not in the published APP repository.

Users may choose git-backed storage for a datastore; APP does not require git operations as part of execution.

### Arbitration Model

The executing agent binds each location to a concrete path or storage surface at runtime. APP manifests declare **what** is needed (roles, constraints, contracts); the agent and user supply **where** it lives.

Contracts, outputs, and skills should refer to logical roles (`userDatastore`, `agentWorkspace`) rather than hard-coded repo-relative paths for persistent or working data.

Example output template:

```yaml
outputs:
  primary:
    type: report
    pathTemplate: "{userDatastore}/reports/{timestamp}-{playbookId}/Report.md"
  runManifest:
    pathTemplate: "{userDatastore}/reports/{timestamp}-{playbookId}/run-manifest.yaml"
```

## Legacy ASP / TradingCoach Remediation

Approved remedies for migrating legacy TradingCoach (ASP) patterns to APP:

| Legacy issue | Approved remedy |
| --- | --- |
| Repo is mutable live workspace (data + reports committed) | APP repo is behavior-only; user datastore and durable run archives live outside repo |
| Hard-coded repo paths and output adapters | Logical roles in contracts/outputs; paths bound from pack-level inputs at execution |
| Single-user product repo | User-agnostic pack; all user state in bound user datastore |
| `capabilities/` + `.asp.yaml` + `capabilityKind` | `skills/<name>/SKILL.md` (Agent Skills); `playbook.app.yaml` references only |
| No pack manifest; `productId` on each artifact | `pack.app.yaml` owns identity, inputs, paths, playbook index |
| Framework spec inside product repo | Framework in `agent-playbook-pack`; TradingCoach becomes `trading-coach.app/` in an APP distribution repo |
| Flat pack tree at repo root | Self-contained `{packId}.app/` instance; repo root is `README.md` + `*.app/` only |
| Git commit-on-run, inventory updates required | Git optional for user datastore; APP does not require git transactions |
| Bootstrap requires long doc chain (`PROJECT.md`, git protocol, etc.) | `pack.app.yaml` + pack README + referenced workflows/contracts/gates |
| Engine rules in repo (`.cursor/rules`, adapter fields) | Consumer platform owns integration; APP stays engine-neutral |
| Contracts split across many root/docs files | Durable rules under `contracts/`; manifests reference by path |
| No scripts during runs; all output in-repo | Prompt-first default; workspace for intermediates; durable output to user datastore |
| Human-only `Manifest.md` run records | Structured `run-manifest.yaml` canonical; `Manifest.md` optional derivative |
| `treatments/` redirects; overlay path variance | Drop treatments layer; playbook-scoped overlays OK; keep canonical playbook ids |

## Pack-Level Inputs

High-level APP dependencies are declared as **pack-level inputs** in top-level APP metadata (`pack.app.yaml`). The executing agent must resolve these before normal playbook use.

Pack-level inputs cover infrastructure and context the whole APP requires, such as:

- `userDatastore` — persistent data location (layout defined in pack-owned contracts, e.g. `contracts/user-datastore-layout.md`)
- `agentWorkspace` — agent working area
- other cross-cutting dependencies (credentials surfaces, external tool endpoints, etc.) as the APP requires

Playbook manifests may declare additional **playbook-level inputs** for a specific user intent (date range, feature flags, per-run options). Pack-level inputs are not duplicated at playbook scope unless a playbook needs a narrowed view of a shared dependency.

Playbook inputs may use `resolveFrom` to bind from a pack-level input id or logical role (for example `userDatastore`). Consumer-specific assembly paths (deployment channels, persona fields, TFY secrets) are resolved by the executing agent or consumer adapter—not declared as APP vocabulary.

Provisional manifest shape (POC; not yet in `schema/app-manifest-v0.1.md`):

```yaml
inputs:
  userDatastore:
    type: datastore
    required: true
    description: User-controlled persistent storage for APP data
  agentWorkspace:
    type: workspace
    required: true
    description: Agent-controlled working area for temp and intermediate artifacts
```

## Shared Behavior Contract

The shared behavior contract is the minimum APP surface that a pack consumer such as TeamFoundry must be able to read and interpret without requiring a specific agent engine.

### Contract Elements

| Element | Purpose |
| --- | --- |
| Pack identity | Stable pack identification, versioning, and description |
| Pack-level inputs | High-level dependencies (datastore, workspace, etc.) the executing agent must resolve |
| Playbook intent | User-intent workflows the pack supports |
| Inputs | Per-playbook values or artifacts that must be resolved before execution |
| Skill references | Local, external, or literal Agent Skills-compatible capabilities |
| Workflows | Shared lifecycle steps such as input discovery and scope confirmation |
| Gates | Preconditions that must clear before execution proceeds |
| Overlays | Optional augmentations such as evaluation or advisory layers |
| Contracts | Data, output, persistence, and artifact rules |
| Outputs | Primary artifacts and optional run manifest location |
| Run manifest | Record of resolved inputs, executed skills, overlays, and outputs |
| Consumption profile | Metadata APP exposes for pack consumers and adapter planning |

### Contract Boundary

APP should be complete enough that TeamFoundry can answer:

- What behavior is being imported?
- What pack-level and playbook-level inputs does it require?
- Which skills and workflows does it compose?
- What outputs and run records should be expected?
- What compatibility or adapter expectations exist?

APP should not require TeamFoundry context such as identity, persona, customer relationship, deployment target, or HQ lifecycle state in order to define the behavior contract itself.

## Pack Layout And Naming

Each APP instance lives in `{packId}.app/` (folder name matches `packId` in `pack.app.yaml`, plus `.app` suffix). Materialized packs use **layer-prefixed** implementation folders so sort order and framework role are visible in the file tree.

### Layer Folders (instance root)

| Folder | Layer | Contents |
| --- | --- | --- |
| `layer0-workflows/` | 0 | Shared lifecycle infrastructure (input discovery, scope confirmation, validation) |
| `layer1-skills/` | 1 | Referenced skills in **agentskills.io** format (`<skill-name>/SKILL.md`, optional `references/`, `scripts/`, `assets/`) |
| `layer2-overlays/` | 2 | Pack-level optional augmentations |
| `layer3-playbooks/` | 3 | User-intent workflows (`<playbook-id>/playbook.app.yaml`) |

### Cross-Cutting Folders (instance root, unprefixed)

| Folder | Contents |
| --- | --- |
| `contracts/` | Durable data, artifact, persistence, and naming rules |
| `gates/` | Behavior-contract preconditions referenced by workflows and playbooks |

### Playbook-Scoped Overlays

Playbook-specific overlays live under `layer3-playbooks/<playbook-id>/overlays/` without a nested `layer2-` prefix.

### Instance Shell

| File | Role |
| --- | --- |
| `APP-EXECUTION.md` | Execution agent guide (instance copy of `docs/app-execution.md`) |
| `pack.app.yaml` | Pack identity, pack-level inputs, playbook index |
| `README.md` | Domain intent and invocation entry for this pack |

Canonical layout is fixed by convention; `pack.app.yaml` lists playbook ids only (no `paths:` block).

Example **distribution repo**:

```text
README.md
trading-coach.app/
  pack.app.yaml
  README.md
  layer0-workflows/
  layer1-skills/
    summarize-holdings/
      SKILL.md
  layer2-overlays/
  layer3-playbooks/
    aggregate-state-review/
      playbook.app.yaml
      overlays/
  contracts/
  gates/
```

`pack.app.yaml` declares path roots:

```yaml
playbooks:
  - aggregate-state-review
  - environment-review
```

Naming rules: layer directory names are fixed (`layer0-workflows`, not `layer0-workflow`); playbook, skill, workflow, and contract files use kebab-case.

## Core Model

### Pack

A pack is the top-level APP unit. It identifies a domain behavior package, declares pack-level inputs, supported playbooks, and provides paths to skills, workflows, overlays, contracts, and manifests.

Draft manifest filename: `pack.app.yaml`

### Playbook

A playbook is a user-intent workflow inside a pack. It declares inputs, required workflows, skill usage, optional overlays, gates, and outputs.

Draft manifest filename: `playbook.app.yaml`

### Skill References

APP should use Agent Skills as the preferred granular capability format. A playbook may reference:

- local skills under `layer1-skills/` (or the path declared in `pack.app.yaml` `paths.skills`)
- external skill references
- lightweight literal skills for embedded procedures

APP should not define a competing skill standard.

Skill procedures describe engine-neutral scope, categories, and artifact intent. Concrete paths, scripts, and inventory locations are mapped by the executing agent or consumer adapter at runtime.

### Workflows And Gates

Workflows are reusable lifecycle infrastructure shared across playbooks, such as input discovery, scope confirmation, and validation.

Gates are explicit preconditions that must clear before a playbook proceeds. They keep invocation, execution, and factory modes distinct.

Gates express **behavior-contract** preconditions (inputs resolved, period confirmed, datastore ready). Identity, persona, and deployment-context preconditions belong to consumer assembly (e.g. TeamFoundry), not APP pack gates.

### Overlays

Overlays are optional augmentations that modify process or output without changing the core playbook intent. Examples include evaluation, advisory, enrichment, policy, and presentation variants.

Overlays may live at pack scope (`layer2-overlays/`) or under `layer3-playbooks/<id>/overlays/`. Legacy treatment redirect layers are not part of APP.

Core output should be defined so a playbook can run without optional overlays.

### Contracts And Outputs

Contracts define durable data, artifact, persistence, and naming rules relative to declared data locations (primarily `userDatastore` for durable artifacts). Durable rules belong in `contracts/` and are referenced from manifests—not scattered across ad hoc root documents.

Outputs describe the primary artifacts a playbook produces and run manifest location, using logical role path templates.

### Run Manifest

A run manifest records what actually happened during one execution: resolved inputs, skills executed, overlays applied, and outputs produced.

The canonical run record is a **structured manifest** (YAML or JSON per APP schema). Human-readable summaries (legacy `Manifest.md` in report folders) may be emitted as optional derivatives for reading or sharing.

### Consumption Profile Expectations

APP should expose enough metadata for TeamFoundry and other consumers to plan ingestion and translation without making APP engine-specific.

Expected consumption-facing metadata includes:

- APP manifest version
- Agent Skills compatibility
- declared runtime compatibility hints where useful
- pack and playbook versions
- skill dependency references
- output and contract expectations
- tool or integration requirements at the behavior level

Engine-native translation details belong in TeamFoundry translation design, not in APP as deployable inventory definitions.

## APP Owns

- Portable behavior and domain workflow packaging in self-contained `{packId}.app/` instances
- Public APP distribution repo shape (`README.md` pack index + `*.app/` only at root)
- Declaration of pack-level inputs and data-location roles
- Playbooks, workflows, gates, overlays, contracts, and outputs
- Skill composition through Agent Skills-compatible references
- Run manifest shape and output expectations
- Compatibility and consumption metadata for pack consumers
- Examples that pressure-test the model

## APP Does Not Own

- Client pull scheduling, local install paths, or copy lifecycle
- The execution runtime or executor implementation (client platform or reference harness)
- Concrete user datastore or agent workspace paths (declared as inputs; bound at execution)
- Persistent data contents or workspace artifact contents
- Git transactions, commit-on-run workflows, or repo inventory maintenance
- Engine-specific routing rules, IDE rules, or consumer adapter wiring
- TeamFoundry assistant storefront, onboarding, or operations
- Persona, identity, customer relationship, or deployment lifecycle
- TFY ingestion, assistant assembly, or HQ-deployable package generation
- Engine-native deployable artifacts such as OpenClaw habits, hooks, or inventory trees
- Runtime execution, permissions, or tool dispatch

## TeamFoundry Realignment Touchpoints

TeamFoundry should consume APP packs as one class of assistant construction input.

APP must therefore express behavior clearly enough for TeamFoundry to:

- ingest a pack without treating APP as a TFY implementation repo
- combine APP behavior with TFY-owned assistant context
- translate assembled assistant inputs into target engine deployables

See `tfy-design.md` for ingestion, assembly, translation, and simulator design.

## Implementation Touchpoints

| Area | Location |
| --- | --- |
| **Execution agent guide** | `docs/app-execution.md` |
| General APP framework docs | `docs/framework.md` |
| Agent Skills integration | `docs/agent-skills-integration.md` |
| Draft manifest schema | `schema/app-manifest-v0.1.md` |
| APP examples | `examples/` |
| Realignment plan and decisions | `teamfoundry-stack-realignment-plan.md` |

## Open Questions

- What pack-level input types beyond `datastore` and `workspace` are needed for TradingCoach POC (e.g. broker credential surface)?
- Should consumption profile metadata live in `pack.app.yaml`, a separate contract file, or both?
- Should APP require local skills to be valid Agent Skills directories during realignment pilots?
