# AgentPlaybookPack

AgentPlaybookPack, abbreviated **APP**, is an open framework for packaging complete agent-run domain workflows.

APP sits above the [Agent Skills](https://agentskills.io) layer. Skills define portable capability units. APP defines how domain playbooks compose skills, tools, workflows, contracts, gates, overlays, and outputs into repeatable user-intent jobs.

This repository is the **APP standards storefront**: framework docs, manifest schema, reference distribution examples, and Pack Store design.

## Start Here

| Audience | Read |
| --- | --- |
| Authors and integrators | [`docs/framework.md`](docs/framework.md) |
| Skill authors | [`docs/app-skills.md`](docs/app-skills.md) |
| Execution agents | [`docs/app-execution.md`](docs/app-execution.md) |
| Full standards index | [`docs/README.md`](docs/README.md) |
| Manifest shape | [`schema/app-manifest-v0.1.md`](schema/app-manifest-v0.1.md) |
| Reference packs | [`examples/`](examples/) — APP distribution repo shape (`README.md` + `*.app/`) |
| Pack Store | [`store/README.md`](store/README.md) |

## Why This Exists

Agent ecosystems already have strong primitives:

- Agent Skills package specialized knowledge and procedures.
- MCP exposes tools, resources, and prompts.
- OpenAPI and JSON Schema describe external APIs and structured data.
- Agent runtimes provide orchestration, memory, delegation, and execution.

APP is not a replacement for those layers. It answers a larger question:

> What should happen end to end when a user asks for a domain outcome?

## Core Claim

An AgentPlaybookPack is a runtime-neutral domain package containing:

- **Playbooks** — user-intent workflows
- **Skills** — granular Agent Skills-compatible capabilities (`layer1-skills/`)
- **Workflows** — shared lifecycle steps such as input discovery and scope confirmation
- **Overlays** — optional augmentations such as evaluation, advisory, or presentation variants
- **Contracts** — data, output, persistence, and governance rules
- **Manifests** — structured metadata for discovery, composition, and run records

## Relationship To Agent Skills

APP uses agentskills.io explicitly for its skill layer. Inside a materialized pack instance:

```text
trading-coach.app/
  layer1-skills/
    normalize-broker-csv/
      SKILL.md
      references/
      scripts/
      assets/
```

Packs may also reference external skills from public hubs, private registries, or literal inline definitions.

## Layer Model

```text
Layer 4  Pack Store      discovery, trust, versioning, distribution
Layer 3  Playbooks       user-intent workflows       layer3-playbooks/
Layer 2  Overlays        optional augmentations        layer2-overlays/; playbook overlays/
Layer 1  Skills          agentskills.io capability     layer1-skills/
Layer 0  Workflows       lifecycle infrastructure      layer0-workflows/
Runtime  Tools           MCP, APIs, shell, browser
```

Cross-cutting `contracts/` and `gates/` live at the pack instance root. Canonical layout is fixed by convention — see [`docs/app-execution.md`](docs/app-execution.md).

## Repository Shape

```text
README.md
docs/                     # APP standards (see docs/README.md)
  framework.md
  app-execution.md
  app-skills.md
  agent-skills-integration.md
  naming.md
  pack-store.md
  tfy-stack-realignment/  # temporary workbench program (outlier)
schema/
  app-manifest-v0.1.md
examples/                 # reference APP distribution repo: README.md + *.app/
  trading-coach.app/
sketches/                 # non-published design sketches
store/                    # Pack Store design home
tools/
  baseline-app-skills.py
  materialize-skill-scripts.py
  migrate-trading-coach.py
  tfy-simulator/          # TFY workbench tool (outlier)
```

## Active Workbench Program

TeamFoundry stack realignment is in progress in this repo as a **temporary architecture workbench**:

- [`docs/tfy-stack-realignment/README.md`](docs/tfy-stack-realignment/README.md)
- Plan: [`docs/tfy-stack-realignment/teamfoundry-stack-realignment-plan.md`](docs/tfy-stack-realignment/teamfoundry-stack-realignment-plan.md)

During this phase, `teamfoundry.ai` remains read-only on adjacent workstations. Accepted APP standards belong in `docs/`, `schema/`, and `examples/` — not only in the realignment folder.

## Status

APP standards baseline and a full reference pack (`examples/trading-coach.app/`) exist. Pack Store listing format and a reference executor are next. See the realignment plan for program status.
