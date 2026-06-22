# APP Execution Guide

This document instructs **execution agents** how to discover, bind inputs, and run this APP pack.

Framework source: `docs/app-execution.md` in the AgentPlaybookPack workbench. This file is the instance copy for self-contained APP repo consumption.

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

**Execution:**

```yaml
directive:
  pack: trading-coach
  playbook: aggregate-state-review
```

**Discovery** (no datastore reads, no reports):

```yaml
directive:
  pack: trading-coach
  mode: discovery
```

---

## Canonical instance layout

Folder names are fixed by convention. Do not expect a `paths:` block in `pack.app.yaml`.

```text
trading-coach.app/
  APP-EXECUTION.md
  pack.app.yaml
  README.md
  layer0-workflows/
  layer1-skills/
  layer2-overlays/
  layer3-playbooks/<playbook-id>/
    playbook.app.yaml
    README.md
    overlays/
  contracts/
  gates/
```

### Manifests

| Artifact | Manifest |
| --- | --- |
| Pack | `pack.app.yaml` |
| Playbook | `layer3-playbooks/<id>/playbook.app.yaml` |
| Skill | `layer1-skills/<id>/` | agentskills.io directory (`SKILL.md`, `scripts/`, `references/`, `assets/`) |
| Workflow, overlay, contract, gate | Markdown only |

Playbook ids in `pack.app.yaml`: `aggregate-state-review`, `environment-review`, `unit-decision-review`, `activity-period-review`, `source-profile`.

---

## Execution sequence

1. Read this file, `pack.app.yaml`, pack `README.md`
2. Open `layer3-playbooks/<playbook-id>/` — read `playbook.app.yaml`
3. Bind `userDatastore` and `agentWorkspace` (mediate if not supplied)
4. Run required `layer0-workflows/` in manifest order
5. Clear gates in `gates/` and playbook manifest
6. Execute `layer1-skills/` per playbook composition — true agentskills.io skills; use bundled `scripts/` when `SKILL.md` instructs
7. Apply playbook `overlays/` when conditions match
8. Write outputs and `run-manifest.yaml` per `contracts/report-artifact-contract.md`

---

## Data locations

- `{userDatastore}` — user-controlled root; layout in `contracts/user-datastore-layout.md`
- `{agentWorkspace}` — agent temp and intermediate artifacts

No persistent data or reports belong in the APP behavior repo.

---

## Discovery rules

- Answer from pack `README.md` and `pack.app.yaml` playbook list
- Map natural language to playbook id + lenses per `contracts/agent-layer-integration.md`
- Do not read datastore or run workflows during discovery

---

## TradingCoach execution notes

- **Skills** — each `layer1-skills/<id>/` is an agentskills.io skill with `scripts/run.py` (Python 3.11+ stdlib); shared lib at `assets/tc-lib/`
- **Prompt-first** — follow `SKILL.md` procedures; run bundled scripts when instructed
- **No ad-hoc scripts** — do not invent executable tooling during a run
- **Report folders** — `{userDatastore}/reports/<timestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>/` per `contracts/report-artifact-contract.md`
- **`timestamp`** — actual wall-clock time at folder creation; never placeholders
- **`Report.md`** — self-contained per report contract; GitHub-safe Mermaid only
- **Run record** — canonical `run-manifest.yaml`; `Manifest.md` optional human derivative
- **Core vs augmented** — `evaluation: false` runs core output only; evaluation overlays add coaching artifacts

### Required contracts for execution

| Contract | Use |
| --- | --- |
| `contracts/user-datastore-layout.md` | Bind `userDatastore` directory structure |
| `contracts/datastore-contract.md` | Merge, validate, period weight reconstruction |
| `contracts/holdings-taxonomy.md` | Rollup lens and mapping gates |
| `contracts/report-artifact-contract.md` | Report folder naming and contents |
| `contracts/persistent-knowledge-model.md` | Knowledge promotion rules |

### Superseded

`contracts/execution-bootstrap.md` — legacy ASP bootstrap; use this file (`APP-EXECUTION.md`) instead.

---

## Version

APP execution guide v0.1 — TradingCoach instance (`pack.app.yaml` `appVersion: "0.1"`).
