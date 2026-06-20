# TeamFoundry Design

## Purpose

This document captures the current design model for how TeamFoundry should evolve during the stack realignment.

TeamFoundry design should describe assistant cultivation, construction, storefront, operations, governance, APP consumption, translation to deployable assistant packages, and simulator-facing behavior. It should not redefine APP as a framework or describe engine-native deployable formats as TeamFoundry source-of-truth behavior contracts.

Baseline strategic intent lives in `teamfoundry-stack-realignment-vision.md`. Active planning, status, work patterns, and decisions live in `teamfoundry-stack-realignment-plan.md`.

## Related Design Documents

- `app-design.md`: APP as the portable behavior contract.

## Documentation Rules

- Keep this design document current-state only.
- Do not narrate design history in this document.
- Do not duplicate the decision log in this document.
- Record meaningful pivots in `teamfoundry-stack-realignment-plan.md`.
- Update this document after a decision so it reflects the accepted current TeamFoundry design.
- Graduate stable TeamFoundry design into TFY docs or implementation artifacts when it becomes durable.

## Status

Drafting

## Current Design Summary

TeamFoundry cultivates, constructs, deploys, and operates assistants for humans who should not need to understand the underlying AI technology stack.

During realignment, TeamFoundry should gain a native APP ingestion layer, assemble assistant instances from modular inputs, and translate assembled context into HQ-deployable packages for target agent layers. OpenClaw is the first concrete translation target.

TeamFoundry remains responsible for assistant storefront, persona cultivation, operations, governance, deployment, and customer experience. APP remains the portable behavior contract layer.

## Core Model

### Foundry

Foundry curates source materials: skills, habits, reflexes, bookshelves, identity, memories, casts, and related inventories.

During realignment, some reusable behavior currently expressed in TFY inventories may be mirrored or translated into APP examples without making Foundry the long-term owner of APP pack definitions.

### Forge

Forge assembles reusable assistant archetypes from casts and inventories into forged bench packages.

Future Forge behavior may consume APP packs as assistant construction input rather than encoding all reusable behavior directly in runtime-shaped inventory trees.

### HQ

HQ instantiates, deploys, commissions, and operates field assistants through artifact-driven request and operations workflows.

APP packs should influence what behavior an assistant carries, but HQ lifecycle, governance, and deployment remain TeamFoundry-owned.

### Assistant Storefront

TeamFoundry presents assistants to humans, handles onboarding and relationship setup, and shields customers from AI infrastructure details.

This is distinct from an APP Pack Store, which distributes reusable behavior packages.

### Assistant Construction Inputs

An assistant instance is assembled from modular inputs:

```text
assistant instance =
  identity
  persona
  knowledge
  APP packs
  Agent Skills
  habits
  policies
  memories
  customer context
  engine profile
  deployment target
```

APP packs are one input type, not the whole assistant definition.

### APP Ingestion Layer

TeamFoundry should ingest APP packs as a native assistant-construction input layer.

Ingestion responsibilities:

- validate pack and playbook manifests
- resolve declared paths and references
- map skill references to local, external, or literal skills
- check compatibility metadata and consumption profile expectations
- surface warnings for missing dependencies or unsupported constructs

Ingestion does not mean APP owns TFY lifecycle or that TFY defers all behavior design to APP.

### Governance And Operations

TeamFoundry retains ownership of request intake, approval, deployment, commissioning, field operations, monitoring, backup, rollback, and support workflows.

## Assumed Translation Flow

TeamFoundry should ingest APP packs as a native assistant-construction input layer, then run a distinct translation path to the HQ-deployable format for the selected target agent layer.

```text
APP Pack
  portable behavior contract

TFY APP Ingestion
  validate pack, resolve metadata, read playbooks, map skills, check compatibility

TFY Native Assistant Assembly Layer
  combine APP behavior with identity, persona, knowledge, policies, memories,
  customer context, governance, deployment intent, and engine profile

Target Translation Path
  convert assembled assistant inputs into engine-specific deployable artifacts

HQ-Deployable Package
  forged or deployable assistant bundle for one or more target agent layers

Agent Engine
  OpenClaw first, other runtimes later
```

Translation should not bypass TeamFoundry assistant assembly context. APP behavior is translated through TFY-owned construction inputs before becoming engine-native deployable artifacts.

The baseline vision pillar name remains APP-to-engine, but the accepted implementation model is TFY-mediated translation. See the plan decision log entry dated 2026-06-20.

## Simulator Model

The local TFY simulator exercises the translation boundary during APP development. It is a development harness in the APP repo, not TeamFoundry itself and not OpenClaw.

### Purpose

Answer this question:

> Can TeamFoundry plausibly ingest this APP pack, assemble assistant context, and produce a target-engine deployment preview?

### Intended Location

```text
tools/tfy-simulator/
  README.md
  output/
```

Preview artifacts should be written to `tools/tfy-simulator/output/` and treated as non-authoritative development outputs.

### Inputs

| Input | Description |
| --- | --- |
| APP pack path | Pack to ingest, usually under `examples/` |
| Playbook id | Playbook to exercise |
| Mock assistant profile | Identity, persona, and role context for assembly |
| Mock customer context | Customer or operator context needed for translation |
| Engine profile | Target engine for preview generation, default `openclaw` |

### Stages

#### Ingest

Read pack and playbook manifests, validate references, and collect compatibility and dependency information.

#### Resolve

Resolve skill references, workflows, gates, overlays, outputs, and declared contracts.

#### Assemble

Combine APP behavior with mock TeamFoundry assistant construction inputs.

#### Translate

Produce target-engine preview artifacts for the selected engine profile.

#### Report

Emit warnings, unsupported mappings, missing dependencies, and a translation manifest summarizing the preview run.

### Expected Outputs

| Output | Description |
| --- | --- |
| `assistant-construction-plan.md` | How TFY would assemble the assistant inputs |
| `translation-manifest.json` | Structured summary of ingest, resolve, assemble, and translate results |
| `engine-preview/` | Engine-specific preview artifacts such as OpenClaw inventory sketches |
| `warnings.txt` | Unsupported constructs, missing context, or adapter gaps |

### Non-Goals

- The simulator is not a runtime engine.
- The simulator is not proof of TFY repo integration.
- The simulator should not require editing `teamfoundry.ai`.
- The simulator should not treat preview artifacts as production deployables.

## TeamFoundry Owns

- Assistant storefront, onboarding, and customer experience
- Persona cultivation and high-quality assistant input content
- Foundry, Forge, and HQ responsibilities
- APP pack ingestion as assistant-construction input
- Assistant assembly context before engine translation
- Translation path to HQ-deployable packages
- Local simulator and translation preview behavior during realignment
- Governance, deployment, commissioning, and field operations

## TeamFoundry Does Not Own

- APP pack and playbook schema as a framework standard
- Agent Skills as a granular capability format
- Portable behavior contracts as the APP source-of-truth layer
- Runtime execution internals inside OpenClaw or other engines

Engine-native deployable formats are translation outputs, not TeamFoundry source-of-truth behavior contracts. APP remains the portable behavior contract layer.

## APP Consumption Assumptions

TeamFoundry expects APP packs to provide the shared behavior contract defined in `app-design.md`.

Minimum consumption assumptions:

- readable pack and playbook manifests
- explicit inputs, gates, outputs, and skill references
- optional overlays and contracts
- consumption profile metadata sufficient for translation planning
- no requirement for TFY-specific persona or deployment data inside APP

## OpenClaw Adapter Preview

OpenClaw is the first engine profile for simulator previews.

Illustrative translation targets:

```text
APP playbook -> OpenClaw skill, prompt workflow, or executable behavior
APP scheduled behavior -> OpenClaw habit or cron prompt
APP event response -> OpenClaw hook or reflex
APP contract -> workspace, report, or persistence convention
APP run manifest -> persisted execution record
```

These mappings are preview targets for the simulator and future TFY adapter work. They are not APP source-of-truth definitions.

## TeamFoundry Reference Map

When reading `teamfoundry.ai` during realignment:

| Path | Use for |
| --- | --- |
| `docs/TeamFoundry-Product-Documentation.md` | Product and lifecycle model |
| `foundry/ops/inventories/skills/` | Existing TFY skills |
| `foundry/ops/casts/teamfoundry-employee.json` | Base employee cast |
| `forge/ops/agents-forged/Warren/` | Investment advisor forged example |
| `forge/ops/agents-forged/Warren/inventories/habits/` | Scheduled report behavior |
| `foundry/ops/inventories/skills/hq-requests/` | HQ request intake behavior |

## Implementation Touchpoints

| Area | Location |
| --- | --- |
| Realignment plan and decisions | `teamfoundry-stack-realignment-plan.md` |
| APP behavior contract | `app-design.md` |
| Simulator implementation | `tools/tfy-simulator/` |
| TFY-derived APP examples | `examples/` |
| Future TFY integration docs | `teamfoundry.ai` after validation phase |

## Open Questions

- What is the first pilot behavior to run through the simulator?
- Which OpenClaw artifact types must the first simulator preview support?
- When should validated design graduate from this document into `teamfoundry.ai`?
