# APP Design

## Purpose

This document captures the current design model for APP as the portable behavior contract in the TeamFoundry stack realignment.

APP design should describe what APP owns as a framework: packs, playbooks, skill references, gates, overlays, contracts, outputs, run manifests, compatibility metadata, examples, and consumption-facing expectations for TeamFoundry and other pack consumers.

Baseline strategic intent lives in `teamfoundry-stack-realignment-vision.md`. Active planning, status, work patterns, and decisions live in `teamfoundry-stack-realignment-plan.md`.

## Related Design Documents

- `tfy-design.md`: TeamFoundry assistant construction, storefront, operations, APP consumption, translation, and simulator model.

## Documentation Rules

- Keep this design document current-state only.
- Do not narrate design history in this document.
- Do not duplicate the design decision log in this document.
- Record meaningful design pivots in `teamfoundry-stack-realignment-plan.md`.
- Update this document after a decision so it reflects the accepted current APP design.
- Graduate stable APP design into `docs/framework.md`, `schema/`, `examples/`, or adapter docs when it becomes durable.

## Framework References

During realignment, use these as the general APP framework references:

- `docs/framework.md`
- `docs/agent-skills-integration.md`
- `docs/naming.md`
- `schema/app-manifest-v0.1.md`
- `examples/trading-coach-mini/`

This document defines the current realignment-specific behavior contract model and may evolve ahead of those files during pilots.

## Status

Drafting

## Current Design Summary

APP is the shared behavior contract between granular Agent Skills and assistant systems such as TeamFoundry.

An APP pack describes reusable assistant behavior and domain workflows in a runtime-neutral way. It defines what should happen for a user intent, which skills and workflows are involved, which gates must clear, which overlays may apply, and which outputs and run records should result.

APP does not deploy assistants, operate storefronts, assemble persona context, or emit engine-native deployable artifacts directly. Those responsibilities belong to TeamFoundry and target agent engines through the translation path described in `tfy-design.md`.

## Shared Behavior Contract

The shared behavior contract is the minimum APP surface that a pack consumer such as TeamFoundry must be able to read and interpret without requiring a specific agent engine.

### Contract Elements

| Element | Purpose |
| --- | --- |
| Pack identity | Stable pack identification, versioning, and description |
| Playbook intent | User-intent workflows the pack supports |
| Inputs | Values or artifacts that must be resolved before execution |
| Skill references | Local, external, or literal Agent Skills-compatible capabilities |
| Workflows | Shared lifecycle steps such as input discovery and scope confirmation |
| Gates | Preconditions that must clear before execution proceeds |
| Overlays | Optional augmentations such as evaluation or advisory layers |
| Contracts | Data, output, persistence, and artifact rules |
| Outputs | Primary artifacts and optional run manifest location |
| Run manifest | Record of resolved inputs, executed skills, overlays, and outputs |
| Consumption profile | Metadata APP exposes for pack consumers and adapter planning |

### Contract Boundary

APP should be complete enough that TeamFoundry can answer:

- What behavior is being imported?
- What inputs and gates does it require?
- Which skills and workflows does it compose?
- What outputs and run records should be expected?
- What compatibility or adapter expectations exist?

APP should not require TeamFoundry context such as identity, persona, customer relationship, deployment target, or HQ lifecycle state in order to define the behavior contract itself.

## Core Model

### Pack

A pack is the top-level APP unit. It identifies a domain behavior package, declares supported playbooks, and provides paths to skills, workflows, overlays, contracts, and manifests.

Draft manifest filename: `pack.app.yaml`

### Playbook

A playbook is a user-intent workflow inside a pack. It declares inputs, required workflows, skill usage, optional overlays, gates, and outputs.

Draft manifest filename: `playbook.app.yaml`

### Skill References

APP should use Agent Skills as the preferred granular capability format. A playbook may reference:

- local skills under `skills/`
- external skill references
- lightweight literal skills for embedded procedures

APP should not define a competing skill standard.

### Workflows And Gates

Workflows are reusable lifecycle infrastructure shared across playbooks, such as input discovery, scope confirmation, and validation.

Gates are explicit preconditions that must clear before a playbook proceeds. They keep invocation, execution, and factory modes distinct.

### Overlays

Overlays are optional augmentations that modify process or output without changing the core playbook intent. Examples include evaluation, advisory, enrichment, policy, and presentation variants.

Core output should be defined so a playbook can run without optional overlays.

### Contracts And Outputs

Contracts define durable data, artifact, persistence, and naming rules. Outputs describe the primary artifacts a playbook produces and any required run manifest location.

### Run Manifest

A run manifest records what actually happened during one execution: resolved inputs, skills executed, overlays applied, and outputs produced.

### Consumption Profile Expectations

APP should expose enough metadata for TeamFoundry and other consumers to plan ingestion and translation without making APP engine-specific.

Expected consumption-facing metadata includes:

- APP manifest version
- Agent Skills compatibility
- declared runtime compatibility hints where useful
- pack and playbook versions
- skill dependency references
- output and contract expectations
- tool or integration requirements at the behavior level

Engine-native translation details belong in TeamFoundry translation design, not in APP as deployable inventory definitions.

## APP Owns

- Portable behavior and domain workflow packaging
- Playbooks, workflows, gates, overlays, contracts, and outputs
- Skill composition through Agent Skills-compatible references
- Run manifest shape and output expectations
- Compatibility and consumption metadata for pack consumers
- Examples that pressure-test the model

## APP Does Not Own

- TeamFoundry assistant storefront, onboarding, or operations
- Persona, identity, customer relationship, or deployment lifecycle
- TFY ingestion, assistant assembly, or HQ-deployable package generation
- Engine-native deployable artifacts such as OpenClaw habits, hooks, or inventory trees
- Runtime execution, permissions, or tool dispatch

## TeamFoundry Realignment Touchpoints

TeamFoundry should consume APP packs as one class of assistant construction input.

APP must therefore express behavior clearly enough for TeamFoundry to:

- ingest a pack without treating APP as a TFY implementation repo
- combine APP behavior with TFY-owned assistant context
- translate assembled assistant inputs into target engine deployables

See `tfy-design.md` for ingestion, assembly, translation, and simulator design.

## Implementation Touchpoints

| Area | Location |
| --- | --- |
| General APP framework docs | `docs/framework.md` |
| Agent Skills integration | `docs/agent-skills-integration.md` |
| Draft manifest schema | `schema/app-manifest-v0.1.md` |
| APP examples | `examples/` |
| Realignment plan and decisions | `teamfoundry-stack-realignment-plan.md` |

## Open Questions

- Should consumption profile metadata live in `pack.app.yaml`, a separate contract file, or both?
- Should APP require local skills to be valid Agent Skills directories during realignment pilots?
- Which pilot behavior should become the first APP example derived from TeamFoundry?
