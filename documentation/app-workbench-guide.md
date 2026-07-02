# APP Workbench Guide

Human-facing guide for users, contributors, and pack authors. **Not** the APP execution standard.

| Need | Read |
| --- | --- |
| Author or validate pack structure | [`../standard/app-authoring.md`](../standard/app-authoring.md) and JSON Schemas in [`../standard/`](../standard/) |
| Execute a pack | [`../standard/app-execution.md`](../standard/app-execution.md), [`../standard/pre-run-checklist.md`](../standard/pre-run-checklist.md), and [`../standard/post-run-checklist.md`](../standard/post-run-checklist.md) |
| See working instances | [`examples/`](examples/) |
| Workbench map | [`../README.md`](../README.md) |

Execution agents learn APP from [`../standard/app-authoring.md`](../standard/app-authoring.md) and [`../standard/app-execution.md`](../standard/app-execution.md), then consume pack instances from a **distribution repo** (`README.md` + `{packId}.app/` at repo root). Reference instances under [`examples/`](examples/) illustrate the format only — they are not execution targets. This document does not define runtime bootstrap or engine integration.

---

## What APP is

**AgentPlaybookPack** (APP) is a portable, runtime-neutral format for domain workflows that agents discover and execute.

A pack describes:

- User intents (playbooks)
- Inputs to resolve
- Skills, workflows, overlays, and contracts to compose
- Primary outputs to produce

APP is **fire-and-forget**: it supplies behavioral instructions for execution agents. It has no ongoing involvement after primary outputs are written. Execution tracking is out of scope.

APP is not a replacement for [Agent Skills](https://agentskills.io), MCP, a runtime orchestrator, or an application framework.

---

## Workbench layout

This repository is the **APP Standards Workbench** — format definition and reference material. It is **not** an APP distribution repo.

```text
agent-playbook-pack/
  README.md           workbench map
  standard/           normative standard (authoring + JSON Schema)
  documentation/      product guide and reference pack instances
    app-workbench-guide.md
    examples/
```

| Folder | Role |
| --- | --- |
| [`standard/`](../standard/) | Authoritative standard. Manifests are YAML; validity is defined by JSON Schema. Includes `app-authoring.md`, `app-execution.md`, `pre-run-checklist.md`, and `post-run-checklist.md`. |
| [`documentation/`](../documentation/) | Product context for humans and format reference instances. |
| [`documentation/examples/`](examples/) | Side-by-side reference instances (format study only; not execution targets). Must conform to `standard/`. |

When `standard/` and an example disagree, **update the example** to match the standard.

---

## Repository shapes

**Distribution repo** (published product):

```text
my-product-app/
  README.md              pack index (user welcome)
  {packId}.app/
```

Only `README.md` and `*.app/` folders at repo root.

**Pack instance** (`{packId}.app/`):

```text
{packId}.app/
  pack.app.yaml          entry manifest
  README.md              user welcome (not execution authority)
  layer0-workflows/
  layer1-skills/
  layer2-overlays/
  layer3-playbooks/<id>/          playbook manifests only (<id>.app.yaml)
  contracts/
```

Same shape in `documentation/examples/` and in a distribution repo.

---

## Vocabulary

| Term | Meaning |
| --- | --- |
| Pack | Domain package: playbooks, skills, workflows, overlays, contracts, manifests |
| Playbook | User-intent workflow (layer 3) |
| Skill | Granular capability — [agentskills.io](https://agentskills.io) directory under `layer1-skills/` |
| Workflow | Shared lifecycle step — markdown under `layer0-workflows/` |
| Overlay | Optional augmentation — markdown under `layer2-overlays/`; referenced from playbook manifest `overlays:` |
| Contract | Durable data, artifact, or naming rule — markdown under `contracts/` |
| Gate | Playbook precondition — declared on `<playbook-id>.app.yaml`; cleared by workflows |
| `{userDatastore}` | User persistent data; bound at execution; never in APP repos |
| `{agentWorkspace}` | Optional ephemeral working area; execution agent chooses when not supplied; cleaned up after the run |

Layer numbering (0–3), manifest fields, and execution outcomes are defined in [`../standard/app-authoring.md`](../standard/app-authoring.md).

---

## Playbook modes

| Mode | Outcome |
| --- | --- |
| Discovery | Answer what the pack can do |
| Execution | Run a playbook after intent is clear |
| Factory | Modify the pack itself |

Keep discovery from triggering datastore reads or report generation.

---

## Core vs augmented output

Every playbook defines **core output** that runs without optional overlays. Overlays add evaluation, enrichment, presentation, policy, or similar behavior when manifest conditions match.

---

## Naming

| Item | Convention |
| --- | --- |
| Product name | AgentPlaybookPack; shorthand **APP** |
| Pack folder | `{packId}.app/` (kebab-case `packId`) |
| Pack manifest | `pack.app.yaml` |
| Playbook manifest | `layer3-playbooks/<playbook-id>/<playbook-id>.app.yaml` |
| Skill directory | `layer1-skills/<skill-id>/` matching `SKILL.md` frontmatter `name` |
| Overlay file | `layer2-overlays/<overlay-id>.md` (kebab-case; referenced from playbook manifest `overlays:`) |
| Playbook / gate ids | kebab-case |

---

## Authoring a pack

1. Read [`../standard/app-authoring.md`](../standard/app-authoring.md).
2. Study [`examples/hello-world.app/`](examples/hello-world.app/) for minimal layer coverage.
3. Create `{packId}.app/` with `pack.app.yaml` as entry.
4. Add layer 0–3 artifacts and `contracts/`; reference them from manifests.
5. Write pack `README.md` as user welcome content — examples and narrative, not a manifest duplicate.
6. Validate manifests:

```bash
pip install -r standard/requirements.txt
python standard/validate-manifests.py path/to/pack.app.yaml path/to/hello-world.app.yaml
```

7. Publish as a distribution repo (`README.md` + `*.app/` only). Example: [hello-world-app](https://github.com/4jeffclark/hello-world-app) from [`hello-world.app`](examples/hello-world.app/).

---

## Contributing to the workbench

- Propose standard changes in [`../standard/app-authoring.md`](../standard/app-authoring.md) and JSON Schemas together.
- Add or update reference instances under [`examples/`](examples/) to exercise standard features.
- Run `python standard/validate-manifests.py` with no arguments to validate all example manifests and layout rules.
- Do not duplicate normative rules in this folder — keep product prose here, standard prose in `standard/`.

---

## Distribution (future)

A Pack Store or registry is not part of the current standard. Distribution today is: a public git repo with `README.md` and one or more `{packId}.app/` folders.
