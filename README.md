# Portable Agent Capability Stacks — PACS Standards Workbench

Entry point for the workbench. Defines the PACS format. **Not** a PACS distribution repo.

**PACS** (Portable Agent Capability Stacks) — portable capability stacks for agent execution.

---

## Workbench layout

```text
agent-playbook-pack/
  README.md           ← this file (workbench map + agent instructions)
  standard/           ← normative PACS standard
  documentation/      ← product guide and reference pack instances
    pacs-workbench-guide.md
    examples/
```

```text
Distribution repo (published product)     Pack instance ({packId}.pacs/)
my-product-app/                           pack.pacs.yaml
  README.md                               README.md
  {packId}.pacs/                           layer0-workflows/
                                          layer1-skills/
                                          layer2-overlays/
                                          layer3-playbooks/
                                          contracts/
```

| Term | Meaning |
| --- | --- |
| **Standards Workbench** | This repo |
| **Distribution repo** | `README.md` + `*.pacs/` only; clients pull read-only copies |
| **Pack instance** | `{packId}.pacs/` — the behavior unit |
| **`userDatastore`** | User persistent data — bound at execution; never in PACS repos |

---

## File scope

| Path | Scope |
| --- | --- |
| [`README.md`](README.md) | Workbench identity, layout, vocabulary, agent instructions (this file) |
| [`standard/pacs-authoring.md`](standard/pacs-authoring.md) | Authoring standard — layout, layers, execution outcomes |
| [`standard/pacs-execution.md`](standard/pacs-execution.md) | Execution guide — refresh, bind, run, pre/post verification |
| [`standard/pre-run-checklist.md`](standard/pre-run-checklist.md) | Contract checklist before execution (workbench and pack refresh) |
| [`standard/post-run-checklist.md`](standard/post-run-checklist.md) | Contract checklist after execution |
| [`standard/pack.manifest.schema.json`](standard/pack.manifest.schema.json) | JSON Schema for `pack.pacs.yaml` |
| [`standard/playbook.manifest.schema.json`](standard/playbook.manifest.schema.json) | JSON Schema for `<playbook-id>.pacs.yaml` |
| [`standard/README.md`](standard/README.md) | Standard folder label |
| [`documentation/examples/`](documentation/examples/) | Reference pack instances |
| [`documentation/pacs-workbench-guide.md`](documentation/pacs-workbench-guide.md) | Workbench product guide for users, contributors, and authors |
| [`documentation/README.md`](documentation/README.md) | Documentation folder index |
| [`documentation/session-transcripts/README.md`](documentation/session-transcripts/README.md) | Session handover catalog (task index only; not in read order) |
| [`documentation/dev-archive/`](documentation/dev-archive/) | Historical session exports and superseded material (not normative; excluded from Cursor indexing) |

---

## Agent instructions

For AI agents working in this repo. Human contributors may also use [`documentation/pacs-workbench-guide.md`](documentation/pacs-workbench-guide.md).

### Agent roles

| Role | Context | Purpose |
| --- | --- | --- |
| **Workbench agent** | This repo | Learn the standard; study reference instances; author or validate packs |
| **Execution agent** | A distribution repo | Learn PACS from [`standard/pacs-authoring.md`](standard/pacs-authoring.md), [`standard/pacs-execution.md`](standard/pacs-execution.md), and checklists; refresh workbench and pack before execution; consume `{packId}.pacs/` manifests and referenced layer artifacts |

`documentation/examples/` is format reference only — **not** an execution target. Published packs live in distribution repos.

### Read order (workbench agents)

| Need | Read |
| --- | --- |
| Authoring standard | [`standard/pacs-authoring.md`](standard/pacs-authoring.md) |
| Execution guide | [`standard/pacs-execution.md`](standard/pacs-execution.md) |
| Pre-run checklist | [`standard/pre-run-checklist.md`](standard/pre-run-checklist.md) |
| Post-run checklist | [`standard/post-run-checklist.md`](standard/post-run-checklist.md) |
| JSON Schemas and validator | [`standard/`](standard/) |
| Human product guide | [`documentation/pacs-workbench-guide.md`](documentation/pacs-workbench-guide.md) |
| Reference pack instances (study) | [`documentation/examples/`](documentation/examples/) |

Pack `README.md` files in `documentation/examples/` are user welcome only — not execution authority.

### Work rules

- Treat `standard/` as normative; when `standard/` and an example disagree, update the example.
- Validate manifests and layout: `python standard/validate-manifests.py` (schema, overlay paths under `layer2-overlays/`, playbook index, forbidden legacy artifacts).
- Gate metadata lives on `<playbook-id>.pacs.yaml` only (no `gates/` folder).
- All overlays live under `layer2-overlays/` (not under `layer3-playbooks/`).
- Pack shell entry is `pack.pacs.yaml`.
- Execution agents read [`standard/pacs-execution.md`](standard/pacs-execution.md), [`standard/pre-run-checklist.md`](standard/pre-run-checklist.md), and [`standard/post-run-checklist.md`](standard/post-run-checklist.md) after the authoring standard; refresh workbench standard and distribution pack before running any playbook unless the run request pins a `ref`.
- PACS is fire-and-forget: behavioral instructions only; no run manifests or execution tracking.
- Use Sketch-Then-Materialize: do not create whole example trees unless explicitly requested.
- Treat `documentation/dev-archive/` as historical only; normative source is `standard/`.
- `documentation/session-transcripts/` is handover only. Read a specific file only when the user cites it; never treat as normative or browse for background.

### Reference instances

| Instance | Workbench role | Published distribution |
| --- | --- | --- |
| [`documentation/examples/hello-world.pacs/`](documentation/examples/hello-world.pacs/) | Minimal layer coverage | [hello-world-app](https://github.com/4jeffclark/hello-world-app) |
