# APP Standards

Normative documentation for [AgentPlaybookPack](https://github.com/4jeffclark/agent-playbook-pack) (APP). This folder defines what APP is, how packs are shaped, and how execution agents run them.

Development workbench material for TeamFoundry alignment lives separately in [`tfy-stack-realignment/`](tfy-stack-realignment/) and is not required to consume or execute APP packs.

## Read Order

| Order | Document | Audience |
| --- | --- | --- |
| 1 | [`framework.md`](framework.md) | Authors, integrators, store builders |
| 2 | [`app-execution.md`](app-execution.md) | Execution agents and reference executors |
| 3 | [`app-skills.md`](app-skills.md) | Skill directories and scripting baseline |
| 4 | [`agent-skills-integration.md`](agent-skills-integration.md) | Skill composition in playbooks |
| 5 | [`naming.md`](naming.md) | Naming and folder conventions |
| 6 | [`../schema/app-manifest-v0.1.md`](../schema/app-manifest-v0.1.md) | Manifest authors |
| 7 | [`pack-store.md`](pack-store.md) | Pack Store design |

## By Role

### Pack authors

1. [`framework.md`](framework.md) — concepts and layer model
2. [`app-skills.md`](app-skills.md) — agentskills.io skill directories and `scripts/` baseline
3. [`naming.md`](naming.md) — `{packId}.app/` and distribution repo rules
3. [`../schema/app-manifest-v0.1.md`](../schema/app-manifest-v0.1.md) — `pack.app.yaml` and `playbook.app.yaml`
4. [`../examples/trading-coach.app/`](../examples/trading-coach.app/) — reference materialized instance

Each published instance includes **`APP-EXECUTION.md`** (copy of [`app-execution.md`](app-execution.md) plus pack-specific notes) so pulled APP repos are self-sufficient.

### Execution agents

1. Pack instance **`APP-EXECUTION.md`**
2. [`app-execution.md`](app-execution.md) — framework baseline when the workbench is available
3. Pack `pack.app.yaml`, playbook manifests, and `contracts/`

Do not require `tfy-stack-realignment/` or other workbench docs during execution.

### Store and distribution

1. [`pack-store.md`](pack-store.md)
2. [`../store/README.md`](../store/README.md)
3. [`../examples/README.md`](../examples/README.md) — reference distribution repo index

## Layout Quick Reference

**APP distribution repo** (what clients pull):

```text
README.md           # pack index
<trading-coach>.app/
```

**APP instance** (`{packId}.app/`):

```text
APP-EXECUTION.md
pack.app.yaml
README.md
layer0-workflows/
layer1-skills/
  <skill-id>/
    SKILL.md
    scripts/
    references/
    assets/
layer2-overlays/
layer3-playbooks/<id>/
  playbook.app.yaml
  overlays/
contracts/
gates/
```

Canonical folder names are convention — omit `paths:` from manifests when using this layout. Details: [`app-execution.md`](app-execution.md).

## Related Repositories

| Repo | Role |
| --- | --- |
| This repo | APP standards, schema, reference examples, store design |
| Domain APP repos | Published `{packId}.app/` instances (behavior only; no user data) |
| `teamfoundry.ai` | TFY runtime reference (read-only during workbench phase) |
