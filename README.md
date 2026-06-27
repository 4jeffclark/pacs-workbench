# AgentPlaybookPack — APP Standards Workbench

Entry point for the workbench. Defines the APP format. **Not** an APP distribution repo.

**APP** (AgentPlaybookPack) packages domain playbooks that compose [Agent Skills](https://agentskills.io), workflows, contracts, gates, overlays, and manifests into runnable user-intent jobs.

---

## Workbench layout

```text
agent-playbook-pack/
  README.md           ← this file (workbench map + agent instructions)
  standard/           ← normative APP standard
  examples/           ← reference pack instances
  documentation/      ← product guide for humans (not APP standard)
```

```text
Distribution repo (published product)     Pack instance ({packId}.app/)
my-product-app/                           pack.app.yaml
  README.md                               README.md
  {packId}.app/                           layer0-workflows/
                                          layer1-skills/
                                          layer2-overlays/
                                          layer3-playbooks/
                                          contracts/
```

| Term | Meaning |
| --- | --- |
| **Standards Workbench** | This repo |
| **Distribution repo** | `README.md` + `*.app/` only; clients pull read-only copies |
| **Pack instance** | `{packId}.app/` — the behavior unit |
| **`userDatastore`** | User persistent data — bound at execution; never in APP repos |

---

## File scope

| Path | Scope |
| --- | --- |
| [`README.md`](README.md) | Workbench identity, layout, vocabulary, agent instructions (this file) |
| [`standard/app-authoring.md`](standard/app-authoring.md) | Authoring standard — layout, layers, execution outcomes |
| [`standard/pack.manifest.schema.json`](standard/pack.manifest.schema.json) | JSON Schema for `pack.app.yaml` |
| [`standard/playbook.manifest.schema.json`](standard/playbook.manifest.schema.json) | JSON Schema for `<playbook-id>.app.yaml` |
| [`standard/README.md`](standard/README.md) | Standard folder label |
| [`examples/`](examples/) | Reference pack instances |
| [`documentation/app-workbench-guide.md`](documentation/app-workbench-guide.md) | Workbench product guide for users, contributors, and authors |
| [`documentation/README.md`](documentation/README.md) | Documentation folder index |

---

## Agent instructions

For AI agents working in this repo. Human contributors may also use [`documentation/app-workbench-guide.md`](documentation/app-workbench-guide.md).

### Agent roles

| Role | Context | Purpose |
| --- | --- | --- |
| **Workbench agent** | This repo | Learn the standard; study reference instances; author or validate packs |
| **Execution agent** | A distribution repo | Learn APP from `standard/app-authoring.md`; consume `{packId}.app/` manifests and referenced layer artifacts |

`examples/` is format reference only — **not** an execution target. Published packs live in distribution repos.

### Read order (workbench agents)

| Need | Read |
| --- | --- |
| Authoring standard | [`standard/app-authoring.md`](standard/app-authoring.md) |
| JSON Schemas and validator | [`standard/`](standard/) |
| Human product guide | [`documentation/app-workbench-guide.md`](documentation/app-workbench-guide.md) |
| Reference pack instances (study) | [`examples/`](examples/) |

Pack `README.md` files in `examples/` are user welcome only — not execution authority.

### Work rules

- Treat `standard/` as normative; when `standard/` and an example disagree, update the example.
- Validate manifests and layout: `python standard/validate-manifests.py` (schema, overlay paths under `layer2-overlays/`, playbook index, forbidden legacy artifacts).
- Gate metadata lives on `<playbook-id>.app.yaml` only (no `gates/` folder).
- All overlays live under `layer2-overlays/` (not under `layer3-playbooks/`).
- Pack shell entry is `pack.app.yaml` (no `APP-EXECUTION.md`).
- APP is fire-and-forget: behavioral instructions only; no run manifests or execution tracking.
- Use Sketch-Then-Materialize: do not create whole example trees unless explicitly requested.

### Reference instances

| Instance | Workbench role | Published distribution |
| --- | --- | --- |
| [`examples/hello-world.app/`](examples/hello-world.app/) | Minimal layer coverage | [hello-world-app](https://github.com/4jeffclark/hello-world-app) |
