# APP Authoring Standard v0.2

AgentPlaybookPack (APP) — portable, runtime-neutral domain workflow packages.

APP is **fire-and-forget**: it supplies behavioral instructions for execution agents. APP has no ongoing involvement in runs after primary outputs are written. Execution tracking is out of scope.

Pack `README.md` is lightweight user documentation. It is not authoritative for execution.

| Audience | Document |
| --- | --- |
| Pack authors | This file |
| Execution agents | [`app-execution.md`](app-execution.md), [`pre-run-checklist.md`](pre-run-checklist.md), and [`post-run-checklist.md`](post-run-checklist.md) |

---

## Repo shapes

```text
Standards Workbench                 Distribution repo (published product)
agent-playbook-pack/                  my-product-app/
  standard/                             README.md
  documentation/                        {packId}.app/
    examples/
```

A **pack instance** (`{packId}.app/`) has the same shape in `documentation/examples/` and in a distribution repo:

```text
{packId}.app/
  pack.app.yaml
  README.md
  layer0-workflows/
  layer1-skills/<id>/SKILL.md
  layer2-overlays/
  layer3-playbooks/<id>/<id>.app.yaml
  contracts/
```

Distribution repos contain only `README.md` and `*.app/` at repo root.

### Execution copy vs authoring source

Distribution repos are **published products**. Execution agents consume them through a **one-way, read-only** local copy: pull (or re-clone) to refresh, then read manifests and run skills. They **do not** edit the execution copy for durable pack changes and **never** commit or push back to the distribution remote from an execution context.

Pack authors work in a **separate authoring workspace** (clone or worktree), commit there, and publish to the distribution remote. Execution agents pull those updates into their read-only cache before the next run. Operational detail: [`app-execution.md`](app-execution.md#distribution-repo-boundary-execution-copy).

---

## Layer model

| Layer | Folder | Contents |
| --- | --- | --- |
| 0 | `layer0-workflows/` | Shared lifecycle infrastructure (input discovery, scope confirmation, validation) |
| 1 | `layer1-skills/` | agentskills.io skill directories |
| 2 | `layer2-overlays/` | Optional augmentations |
| 3 | `layer3-playbooks/<id>/` | Playbook manifests |

| Cross-cutting | Folder | Contents |
| --- | --- | --- |
| Contracts | `contracts/` | Durable data, artifact, persistence, and naming rules |
| Gates | `<playbook-id>.app.yaml` | Gate metadata (`id`, `description`, optional `after`, `when`) |

All overlays live under `layer2-overlays/`. Playbooks reference them from manifest `overlays:` with `when:` conditions.

---

## Execution outcomes

Given a pack instance address and a resolved playbook, execution must:

1. Refresh workbench standard and distribution pack per [`pre-run-checklist.md`](pre-run-checklist.md) before reading manifests (unless discovery-only with no execution handoff).
2. Read `pack.app.yaml`, then `layer3-playbooks/<id>/<id>.app.yaml`, then manifest-referenced artifacts only.
3. Bind required pack-level inputs (`userDatastore`; `agentWorkspace` when supplied or agent-selected); declare [execution closure](app-execution.md#execution-closure-and-memory-planes); resolve playbook inputs before core output.
4. Run required workflows; clear gates per playbook manifest.
5. Execute referenced skills per each skill's `SKILL.md`.
6. Apply overlays when manifest conditions match.
7. Write primary outputs per playbook manifest and referenced output contracts.
8. Self-verify per [`post-run-checklist.md`](post-run-checklist.md).

Operational detail: [`app-execution.md`](app-execution.md).

Pack instances are consumed from **distribution repos** (`README.md` + `{packId}.app/` at repo root). See [Repo shapes](#repo-shapes).

### Data locations

| Role | In APP repo? |
| --- | --- |
| Behavior contract | Yes (read-only) |
| `{userDatastore}` | No — bind at execution |
| `{agentWorkspace}` | No — bind at execution |

### Rules

- Prompt-first; run bundled scripts only when `SKILL.md` instructs.
- No ad-hoc scripts during a run.
- Git is not required.
- Core output runs without optional overlays unless playbook inputs enable them.

### Modes

| Mode | Outcome |
| --- | --- |
| Discovery | Answer what the pack can do; do not read datastore or write reports |
| Execution | Run a playbook after user intent is clear; treat the provisioned distribution copy as read-only |
| Factory | Modify the pack in an authoring workspace; publish to the distribution remote — not in the execution cache |

**Discovery → execution handoff:** Confirm target playbook, bindings, and resolved inputs before binding `{userDatastore}` or running workflows. Discovery must not write durable outputs. See [`app-execution.md`](app-execution.md#modes-and-handoff).

---

## Pack manifest

File: `pack.app.yaml` (YAML on disk)

Machine contract: [`pack.manifest.schema.json`](pack.manifest.schema.json)

```yaml
appVersion: "0.1"
kind: pack
packId: hello-world
name: Hello World
version: "1.0.0"
description: Minimal reference instance.
license: MIT

compatibility:
  agentSkills: ">=1.0"

inputs:
  userDatastore:
    type: datastore
    required: true
    description: User-controlled persistent storage
    layoutContract: contracts/user-datastore-layout.md
  agentWorkspace:
    type: workspace
    required: false
    description: >-
      Optional. Ephemeral temp and intermediate artifacts. Omit when the
      execution agent chooses and cleans up its own workspace (default).

playbooks:
  - hello-world
```

Canonical layout is convention. Omit path roots when using the standard tree.

---

## Playbook manifest

File: `layer3-playbooks/<id>/<id>.app.yaml` (YAML on disk)

The manifest filename must match the playbook `id` and parent folder name.

Machine contract: [`playbook.manifest.schema.json`](playbook.manifest.schema.json)

```yaml
appVersion: "0.1"
kind: playbook
id: hello-world
packId: hello-world
version: "1.0.0"
description: Produce a greeting report for a named recipient.
playbookReportId: HelloWorld

inputs:
  recipient:
    type: string
    default: World
    description: Name to greet
  friendly:
    type: boolean
    default: false
    description: Include friendly sign-off overlay
  banner:
    type: boolean
    default: false
    description: Include welcome banner overlay

requires:
  - workflow: ../../layer0-workflows/input-discovery

uses:
  - skill: ../../layer1-skills/compose-greeting

overlays:
  - id: welcome-banner
    path: ../../layer2-overlays/welcome-banner.md
    kind: presentation
    when: banner == true
  - id: friendly-sign-off
    path: ../../layer2-overlays/friendly-sign-off.md
    kind: enrichment
    when: friendly == true

gates:
  - id: inputs-resolved
    after: input-discovery
    description: Playbook inputs resolved or confirmed with defaults
  - id: output-written
    after: outputs
    description: Primary report written per output contract

outputs:
  primary:
    type: report
    pathTemplate: "{userDatastore}/reports/{timestamp}-HelloWorld/Report.md"
    contract: contracts/output-artifact-contract.md
```

### Composition verbs

| Verb | Meaning |
| --- | --- |
| `requires` | Must complete before the playbook proceeds |
| `uses` | Invoked by the playbook |
| `embeds` | Included inline in the output artifact |
| `references` | Linked or optionally consulted |
| `overlays` | Optional augmentation units |

### Skill references (`uses:`)

Local skill (default):

```yaml
uses:
  - skill: ../../layer1-skills/normalize-broker-csv
```

External skill reference:

```yaml
uses:
  - skillRef:
      type: git
      uri: https://github.com/example/agent-skills.git
      path: finance/normalize-broker-csv
      version: v1.2.0
```

Literal skill (small pack-local procedures):

```yaml
uses:
  - skillLiteral:
      name: classify-position-intent
      description: Classify a position note as trade, investment, hedge, or cash management.
      instructions: |
        Read the position note and assign one primary intent.
```

Extract to a full `layer1-skills/<id>/` directory when the procedure grows.

Reference types for `skillRef`: `git`, `registry`, `url`, `local`.

### Default resolution policies

When the user does not specify a value (especially date ranges), execution agents need a declared policy — not an invented one. Playbooks may set `defaultResolution` at the manifest root:

```yaml
defaultResolution:
  period: fullAvailableRange
```

| Policy | Meaning |
| --- | --- |
| `fullAvailableRange` | Use the widest range available in the bound datastore |
| `latestCalendarMonth` | Use the most recent complete calendar month present in data |
| `requireExplicit` | Do not infer; treat as pending unless manifest `default` applies |

Omit `defaultResolution` when every input has an explicit manifest `default` and no period inference is needed (as in hello-world). Layer 0 input-discovery workflows should reference this block when reconciling period inputs.

### Gates and evidence

Workflows and skills **clear** gates by id; the playbook manifest **defines** them.

| Field | Required | Description |
| --- | --- | --- |
| `id` | Yes | Stable gate identifier referenced by workflows |
| `description` | Yes | Short behavior-contract summary |
| `after` | No | Workflow id or phase (`outputs`) that clears the gate |
| `when` | No | Condition when the gate applies (omit when always required) |

Procedural detail belongs in the workflow or contract that enforces the gate—not in YAML.

**Workflow kinds and minimum evidence:**

| Kind | Companion script | Minimum evidence to clear a gate |
| --- | --- | --- |
| Agent-only procedure | Not required | Procedure steps completed; gate id noted in run attestation |
| Script-backed procedure | Required when Procedure says run script | Script outputs on disk per `SKILL.md` Outputs; or contract-defined artifact |
| Domain validation (merge, layout) | Recommended when checks are machine-verifiable | Contract-defined artifact (e.g. validation summary, range manifest) |

Execution agents self-attest pre-run refresh per [`pre-run-checklist.md`](pre-run-checklist.md), gate clearance, and post-run verification per [`post-run-checklist.md`](post-run-checklist.md).

---

## Layer 1 — Skills

`layer1-skills/` directories are [agentskills.io](https://agentskills.io/specification) Agent Skills. APP composes skills; it does not define an alternate skill format.

```text
layer1-skills/<skill-id>/
  SKILL.md          # required
  scripts/          # optional
  references/       # optional
  assets/           # optional
```

When a pack ships bundled executables, include `scripts/run.py` and document it in the **Scripts** section of `SKILL.md`. Scripts must accept `--datastore` and `--workspace` as the canonical path interface. Document cross-platform invocation (Unix shell and PowerShell) or flag-only examples. See [`app-execution.md`](app-execution.md#script-invocation).

### `SKILL.md` frontmatter

| Field | Rule |
| --- | --- |
| `name` | kebab-case; must match directory name |
| `description` | what the skill does and when to use it |
| `compatibility` | environment requirements when non-obvious |
| `outputCompleteness` | optional — `complete` or `scaffold` (see below) |
| `metadata` | string key-value pairs only |

**`outputCompleteness`:**

| Value | Meaning |
| --- | --- |
| `complete` | Script or procedure produces final artifact content |
| `scaffold` | Script produces structure or indexes; agent fills narrative per Procedure |

Omit when a bundled script produces all listed outputs (`complete` implied). Use `scaffold` when the agent must synthesize report sections from partial CSV or template output.

### `SKILL.md` body sections

1. **Procedure** — step-by-step instructions
2. **Scripts** — bundled scripts and how to run them (state "none" if empty)
3. **References** — pointers to `references/` or pack `contracts/`
4. **Outputs** — artifacts produced
5. **Used by** — playbooks that invoke this skill (pack documentation)

Scripts read/write `{userDatastore}` and `{agentWorkspace}` — not the APP behavior repo.

---

## Layer 0 — Workflows

Markdown files under `layer0-workflows/`. Referenced from playbook manifest `requires:`.

Each workflow declares its id, layer, purpose, and procedure. Workflows clear gates by id per the playbook manifest.

---

## Layer 2 — Overlays

Markdown files under `layer2-overlays/`.

Referenced from playbook manifest `overlays:` with `when:` conditions. Core output must be defined so a playbook can run without optional overlays.

---

## Contracts

Markdown under `contracts/`. Referenced from manifests and layer artifacts.

Contracts define durable data layout, artifact shape, persistence rules, and naming conventions relative to `{userDatastore}` and `{agentWorkspace}`.

Primary report outputs use timestamped folders under `{userDatastore}/reports/` unless a contract specifies otherwise.

### Execution closure (author guidance)

Execution agents treat `{userDatastore}` as partially readable — only paths declared by pack contracts and the active playbook's resolved inputs belong in the run [closure set](app-execution.md#closure-set-default). Authors should make read scope explicit:

- **Layout contracts** — document which `{userDatastore}` subtrees skills and playbooks may read (raw, canonical, knowledge, registries).
- **Persistence contracts** — distinguish durable knowledge (for example `knowledge/`) from execution-local reports; state that future runs inherit from promoted knowledge, not from searching prior report folders.
- **Continuity inputs** — when a playbook legitimately reads prior deliverables, declare a playbook input (for example `priorReportPath`, `baselineRunId`) or reference a layer 0 workflow that names required evidence. Do not rely on agents inferring continuity from workspace search.
- **Delivery contracts** — "union of required sections" means the **output contract section list**, not prose copied from a prior run folder.

Packs may add a dedicated `contracts/execution-datastore-read-scope.md` when layout and persistence contracts do not suffice.

---

## Manifest kinds

| Kind | File | Schema |
| --- | --- | --- |
| `pack` | `pack.app.yaml` | [`pack.manifest.schema.json`](pack.manifest.schema.json) |
| `playbook` | `<playbook-id>.app.yaml` | [`playbook.manifest.schema.json`](playbook.manifest.schema.json) |

APP does not use a `skill` manifest kind. Skills use agentskills.io `SKILL.md`.

### Manifest format and validation

- **On-disk format:** YAML (`pack.app.yaml`, `<playbook-id>.app.yaml`).
- **Schema format:** JSON Schema in this folder (industry-standard machine contract).
- **Validation:** Parse YAML to a JSON data model, then validate against the schema.

```bash
pip install pyyaml jsonschema
python standard/validate-manifests.py
```

Validate specific files by passing paths. With no arguments, validates all manifests under `documentation/examples/` and checks layout rules (overlay paths under `layer2-overlays/`, playbook index, forbidden legacy artifacts).

**Execution agents do not run this validator** before executing a distribution pack. Authoring and CI only, unless a run request or pack README explicitly requires it.

JSON may be used at tool or API boundaries later; YAML remains the canonical format in distribution repos and examples.

---

## Version

APP authoring standard v0.2.
