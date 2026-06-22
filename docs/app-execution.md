# APP Execution Guide

This document instructs **execution agents** how to discover, bind inputs, and run APP packs. It is the runtime-facing APP contract.

Development and realignment design lives elsewhere (`docs/tfy-stack-realignment/app-design.md`). This guide is what an executor or agent should follow when pointed at an APP distribution repo.

Each materialized pack instance should include a copy of this guide as `APP-EXECUTION.md` at the instance root so a pulled APP repo is self-sufficient without the framework workbench.

---

## Execution interface

An APP run is invoked with:

| Input | Required | Description |
| --- | --- | --- |
| `appRepo` | Yes | Path or pulled copy of an APP distribution repo |
| `directive` | Yes | Target pack and playbook, or natural-language intent |
| `inputs` | No | Partial pack-level and playbook-level parameters |

The executing agent **mediates** all omitted inputs: `userDatastore`, `agentWorkspace`, remaining manifest inputs, and workflow-discovered options.

### Directive shapes

**Execution** — run a playbook:

```yaml
directive:
  pack: trading-coach
  playbook: aggregate-state-review
```

Or natural-language intent; resolve to a playbook using the pack `README.md` and `pack.app.yaml` playbook list before reading datastore content.

**Discovery** — catalog only (no datastore reads, no report generation):

```yaml
directive:
  pack: trading-coach
  mode: discovery
```

**Factory** — modify the pack (out of scope for default execution agents unless explicitly requested).

---

## APP distribution repo layout

Canonical top level — **only**:

```text
README.md           # index of packs (*.app/)
<trading-coach>.app/
<other-pack>.app/
```

1. Read repo `README.md` for the pack index.
2. Open `{packId}.app/` for the selected pack.

No other top-level files belong in a published APP distribution repo.

---

## APP instance layout (canonical)

Folder names are **fixed by convention**. Do not expect a `paths:` block in `pack.app.yaml`; resolve locations from this layout.

```text
{packId}.app/
  APP-EXECUTION.md       # this guide (instance copy)
  pack.app.yaml          # pack manifest — required
  README.md              # pack intent and playbook catalog
  layer0-workflows/      # shared lifecycle procedures (.md)
  layer1-skills/         # agentskills.io skill directories (SKILL.md)
  layer2-overlays/       # pack-level overlays (optional; often empty)
  layer3-playbooks/
    <playbook-id>/
      playbook.app.yaml  # playbook manifest — required
      README.md          # playbook design reference
      overlays/          # playbook-scoped overlays (.md)
  contracts/             # durable rules (.md)
  gates/                 # gate definitions (.md)
```

### What has an APP manifest

| Artifact | Manifest | Notes |
| --- | --- | --- |
| Pack | `pack.app.yaml` | Identity, `inputs`, playbook index |
| Playbook | `playbook.app.yaml` | Composition, gates, outputs |
| Skill | `layer1-skills/<id>/SKILL.md` | agentskills.io frontmatter only |
| Workflow, overlay, contract, gate | **None** | Markdown procedures; referenced by path or id |

### Playbook location convention

```text
layer3-playbooks/<playbook-id>/playbook.app.yaml
```

Playbook ids in `pack.app.yaml` are listed by id; paths follow the convention above.

### Skill location convention

```text
layer1-skills/<skill-id>/SKILL.md
```

### Workflow location convention

```text
layer0-workflows/<workflow-id>.md
```

Playbook `requires` entries reference workflows relative to the playbook manifest, typically `../../layer0-workflows/<workflow-id>`.

---

## Execution sequence

1. **Locate pack** — `{appRepo}/{packId}.app/`
2. **Read** `APP-EXECUTION.md`, `pack.app.yaml`, pack `README.md`
3. **Resolve directive** — select `layer3-playbooks/<playbook-id>/`
4. **Read** `playbook.app.yaml` and playbook `README.md`
5. **Bind pack-level inputs** from `inputs` or mediate:
   - `userDatastore` — persistent storage (layout per pack contract, e.g. `contracts/user-datastore-layout.md`)
   - `agentWorkspace` — temp and intermediate artifacts
6. **Run required workflows** (`layer0-workflows/`) in order: input discovery, period confirmation, datastore merge, etc.
7. **Clear gates** — verify preconditions in `gates/` and playbook manifest
8. **Execute skills** — follow `layer1-skills/*/SKILL.md` procedures
9. **Apply overlays** — only when playbook manifest conditions match
10. **Write outputs** — to paths from `playbook.app.yaml` `outputs` templates (`{userDatastore}`, `{agentWorkspace}`, `{timestamp}`, resolved playbook inputs)
11. **Write run manifest** — structured `run-manifest.yaml` per pack output contract

---

## Data locations

| Role | Controller | In APP repo? |
| --- | --- | --- |
| Behavior contract | APP instance | Yes (read-only local copy) |
| `userDatastore` | User | **No** — bind at execution |
| `agentWorkspace` | Executing agent | **No** — bind at execution |

Substitute logical roles in contracts, skills, and output templates:

- `{userDatastore}` — pack-bound persistent root
- `{agentWorkspace}` — agent-chosen working area

Pack-specific subdirectory layout under `userDatastore` is defined in that pack's contracts (not by the framework).

---

## Discovery rules

- Answer from repo `README.md`, pack `README.md`, and `pack.app.yaml` playbook list.
- Do **not** read `userDatastore` content during discovery.
- Do **not** start workflows, generate reports, or bind workspaces during discovery.
- Do **not** require framework workbench docs (`docs/tfy-stack-realignment/`, etc.).

---

## Execution rules

- **Prompt-first** — follow skill and workflow markdown; workspace artifacts are optional intermediates.
- **No git required** — APP does not require commit-on-run unless the user chooses git-backed storage.
- **Core vs augmented** — run core outputs without optional overlays unless playbook inputs request them.
- **Structured run record** — canonical record is `run-manifest.yaml`; human summaries are optional derivatives.

---

## Pack-specific contracts

After reading this guide, read pack contracts as referenced by manifests:

- `contracts/user-datastore-layout.md` — where persistent data lives under `userDatastore`
- `contracts/datastore-contract.md` — data merge and validation rules
- `contracts/report-artifact-contract.md` — report folder and artifact rules
- Other `contracts/*.md` as referenced by playbooks and skills

Domain execution details belong in pack contracts and playbooks, not in this framework guide.

---

## What not to read by default

| Path | Reason |
| --- | --- |
| Framework workbench (`docs/tfy-stack-realignment/`) | Development design, not execution |
| Other packs' `.app/` folders | Unless multi-pack run |
| Prior `{userDatastore}` reports | Unless user supplies as context |

---

## Version

APP execution guide v0.1 — aligns with `appVersion: "0.1"` manifests.
