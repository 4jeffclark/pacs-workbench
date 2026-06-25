# AgentPlaybookPack — APP Standards Workbench

Entry point for the workbench. Defines the APP format. **Not** an APP distribution repo.

**APP** (AgentPlaybookPack) packages domain playbooks that compose [Agent Skills](https://agentskills.io), workflows, contracts, gates, overlays, and manifests into runnable user-intent jobs.

---

## Workbench layout

```text
agent-playbook-pack/
  README.md           ← this file (workbench map)
  standard/           ← normative APP standard
  examples/           ← reference pack instances
  documentation/      ← product guide for humans (not APP standard)
```

```text
Distribution repo (published product)     Pack instance ({packId}.app/)
my-product-app/                           pack.app.yaml
  README.md                               README.md
  hello-world.app/                        layer0-workflows/
  portfolio-coach.app/                    layer1-skills/
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
| [`README.md`](README.md) | Workbench identity, layout, vocabulary (this file) |
| [`standard/app-authoring.md`](standard/app-authoring.md) | Authoring standard — layout, layers, execution outcomes |
| [`standard/pack.manifest.schema.json`](standard/pack.manifest.schema.json) | JSON Schema for `pack.app.yaml` |
| [`standard/playbook.manifest.schema.json`](standard/playbook.manifest.schema.json) | JSON Schema for `<playbook-id>.app.yaml` |
| [`standard/README.md`](standard/README.md) | Standard folder label |
| [`examples/`](examples/) | Reference pack instances |
| [`documentation/app-workbench-guide.md`](documentation/app-workbench-guide.md) | Workbench product guide for users, contributors, and authors |
| [`documentation/README.md`](documentation/README.md) | Documentation folder index |
