# AgentPlaybookPack

AgentPlaybookPack, abbreviated APP, is a proposed open framework for packaging complete agent-run domain workflows.

APP is intentionally positioned above the Agent Skills layer. Agent Skills define portable capability units. APP defines how domain playbooks compose skills, tools, workflows, contracts, gates, overlays, and outputs into repeatable user-intent jobs.

## Why This Exists

Agent ecosystems already have strong primitives:

- Agent Skills package specialized knowledge and procedures.
- MCP exposes tools, resources, and prompts.
- OpenAPI and JSON Schema describe external APIs and structured data.
- Agent runtimes provide orchestration, memory, delegation, and execution.

APP is not a replacement for those layers. It is a product and workflow packaging layer that helps agents answer a larger question:

> What should happen end to end when a user asks for a domain outcome?

## Core Claim

An AgentPlaybookPack is a runtime-neutral domain package containing:

- Playbooks: user-intent workflows
- Skills: granular Agent Skills-compatible capabilities
- Workflows: shared lifecycle steps such as input discovery and scope confirmation
- Overlays: optional augmentations such as evaluation, advisory, policy, or presentation variants
- Contracts: data, output, persistence, and governance rules
- Manifests: structured metadata for discovery, composition, and run records
- Examples: reference packs and expected outputs

## Relationship To Agent Skills

APP should use the agentskills.io structure explicitly for its granular skill layer.

Local skills can be stored as Agent Skills directories:

```text
skills/
  normalize-broker-csv/
    SKILL.md
    references/
    scripts/
    assets/
```

Packs can also reference skills from public repositories, private registries, or literal inline definitions when a full local skill directory is not needed.

## Proposed Layering

```text
Layer 4  Pack Store      discovery, trust, versioning, distribution
Layer 3  Playbooks       user-intent workflows
Layer 2  Overlays        optional augmentations
Layer 1  Skills          agentskills.io-compatible capability units
Layer 0  Workflows       lifecycle infrastructure and gates
Runtime  Tools           MCP, APIs, shell, browser, databases
```

## Initial Repository Shape

```text
README.md
docs/
  framework.md
  agent-skills-integration.md
  pack-store.md
schema/
  app-manifest-v0.1.md
examples/
  trading-coach-mini/
store/
  README.md
```

## Status

This is a baseline concept scaffold for local iteration before the first commit of a standalone APP framework repository.
