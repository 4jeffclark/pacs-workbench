# TeamFoundry Stack Realignment Vision

## Executive Thesis

TeamFoundry cultivates, constructs, deploys, and operates assistants for humans who should not need to understand the underlying AI technology stack.

AgentPlaybookPack, abbreviated APP, should become a portable behavior and domain workflow contract that TeamFoundry can consume when assembling assistants. APP packages reusable assistant behaviors, playbooks, gates, overlays, contracts, outputs, and run records. Agent Skills package granular capabilities. Agent engines such as OpenClaw, Cursor, and future runtimes execute those behaviors through adapters and runtime profiles.

The near-term realignment should use the APP repository as a temporary architecture workbench because APP sits between the Agent Skills universe and TeamFoundry. The long-term goal is not a permanent multi-repo control relationship. APP and TeamFoundry should stand on their own, connected by documented contracts and translation boundaries.

## Current Tension

TeamFoundry's long-term intent is to be agent-layer neutral. Its current proof-of-concept implementation has naturally drifted toward OpenClaw because OpenClaw is the first working agent layer and provides useful native primitives: Agent Skills-shaped skills, habits, hooks, memory, persistence, tool execution, and assistant runtime integration.

That drift has created useful progress, but it also creates design pressure:

- Reusable assistant behavior is sometimes expressed in OpenClaw-shaped inventory structures before the behavior contract itself is clear.
- TeamFoundry carries persona, behavior, knowledge, habits, request workflows, deployment operations, and engine installation concerns in one conceptual space.
- OpenClaw-specific mechanics can obscure which parts of TeamFoundry are durable assistant product concepts and which parts are runtime implementation details.
- APP is emerging as a better place to define portable domain behavior and workflow packaging than TeamFoundry itself.

The realignment opportunity is to let TeamFoundry rely more on APP for portable behavior packaging while keeping TeamFoundry focused on assistant cultivation, construction, storefront, deployment, operations, and customer experience.

## Target Stack Model

```text
Human Experience
  Assistant interaction, onboarding, outcomes, support

TeamFoundry
  Assistant storefront, curation, construction, deployment, operations

AgentPlaybookPack
  Reusable assistant behaviors, domain playbooks, gates, overlays, outputs

Agent Skills
  Portable granular capabilities and procedures

Agent Engine
  OpenClaw today, Cursor or other runtimes later

Tools, MCP, APIs, Shell, Channels
  Concrete data access, action surfaces, integrations, transport
```

APP should not sit above TeamFoundry as a management layer. TeamFoundry should not sit below APP as an implementation detail. Instead, TeamFoundry should be able to consume APP packs as one class of assistant construction input.

## Layer Responsibilities

### Human Experience

Humans experience assistants, not agent infrastructure. A customer should interact with an assistant through the intended channel and outcome model without needing to understand APP manifests, OpenClaw inventories, Agent Skills, deployment requests, or runtime adapters.

### TeamFoundry

TeamFoundry owns assistant productization:

- Assistant storefront and customer-facing positioning
- Assistant selection, onboarding, and handoff
- Persona cultivation and high-quality input content
- Knowledge, behavior, self-learning habits, and operating norms
- Construction of modular assistant instances
- Deployment, commissioning, field operations, monitoring, backup, rollback, and support
- Governance and artifact-driven operational workflows

Within the current TeamFoundry model, Foundry curates source materials, Forge assembles reusable assistant archetypes, and HQ instantiates, deploys, commissions, and operates field assistants. The realignment should preserve those durable responsibilities while reducing unnecessary coupling to any one runtime's native inventory format.

TeamFoundry should cultivate assistant-layer input content that can be translated into concrete agent instances. It may use APP packs, Agent Skills, policies, memories, identities, habits, and engine profiles as construction materials.

### AgentPlaybookPack

APP owns portable behavior and workflow packaging:

- Domain playbooks and user-intent workflows
- Reusable workflow gates such as input discovery, scope confirmation, and validation
- Composition of Agent Skills into larger outcomes
- Optional overlays such as evaluation, advisory, policy, enrichment, and presentation variants
- Output contracts and run manifests
- Compatibility metadata for engine adapters and pack consumers
- Examples that pressure-test the model without making APP a persona factory

APP should remain runtime-neutral. It can describe engine compatibility and adapter expectations, but it should not require OpenClaw or any single agent layer.

### Agent Skills

Agent Skills remain the preferred granular capability format. Both APP and OpenClaw already align with the `agentskills.io` skill shape, which creates an automation opportunity: skills can be curated once, referenced by APP packs, and installed or activated by compatible agent engines.

APP should reference local skills, external skill references, or lightweight literal skills without creating a competing skill standard.

### Agent Engine

An agent engine executes assistant behavior. OpenClaw is the first practical target and proof-of-concept agent layer. Future engines could include Cursor-based agents, hosted assistant runtimes, or custom execution systems.

The engine owns runtime mechanics:

- Session lifecycle
- Tool dispatch
- Memory hydration and persistence
- Hooks, cron, or event systems
- Filesystem conventions
- Channel integrations
- Permission enforcement and execution policy

APP should express behavior intent. Engine adapters should translate that intent into runtime-native artifacts.

### Pack Store And TFY Storefront

A Pack Store and the TeamFoundry storefront are related but distinct.

A Pack Store helps discover, validate, trust, version, and distribute reusable APP packs. It focuses on behavior packages and their dependencies.

The TeamFoundry storefront offers assistants to humans. It focuses on assistant outcomes, customer fit, onboarding, deployment, and ongoing service. A TeamFoundry assistant may include one or more APP packs, but it is more than a pack listing.

## Temporary Working Strategy

The near-term work should use side-by-side independent repositories on one workstation:

```text
C:\code\agent-playbook-pack
C:\code\teamfoundry.ai
C:\code\openclaw
```

The APP repository is the temporary architecture workbench because it is the neutral middle layer between Agent Skills and TeamFoundry. This arrangement supports cross-repo reasoning while preserving independent git histories, remotes, branches, and release paths.

This should not become a monorepo, submodule structure, or permanent dependency layout. Once the major conceptual changes taper off, each repository should carry only its own durable responsibilities.

## Long-Term Independence Model

APP and TeamFoundry should stand independently:

- APP defines the portable playbook-pack framework, examples, manifests, compatibility metadata, and adapter concepts.
- TeamFoundry defines assistant curation, construction, storefront, operations, governance, deployment, and field lifecycle.
- OpenClaw defines one concrete agent engine implementation and native runtime primitives.
- Agent Skills remain reusable capability units across APP, OpenClaw, and other compatible systems.

The long-term relationship should be contractual rather than organizational. TeamFoundry should be able to consume a versioned APP pack, translate it into a target engine profile, and include it in an assistant instance without APP owning TeamFoundry's lifecycle.

## Roadmap Pillars

### 1. APP As The Shared Behavior Contract

Define APP as the neutral behavior contract between granular skills and assistant systems. APP should describe complete user-intent workflows without taking ownership of assistant storefront, deployment, or runtime execution.

### 2. TFY Skills Migration To APP-Compatible Skills

Migrate, mirror, or normalize TeamFoundry skills toward APP-compatible Agent Skills shape. This does not mean APP permanently owns TFY skills. It means TFY skills should become portable enough for APP packs to compose and for compatible engines to activate.

### 3. Base Persona And Employee Behavior Realignment

Separate foundational TeamFoundry constructs such as TeamFoundry Employee into clearer units:

- Identity and persona content that remains TeamFoundry-owned
- Reusable assistant behavior that can become APP-compatible pack content or examples
- Runtime activation details that belong to engine adapters
- Operational governance that remains TeamFoundry-owned

APP examples may include a base assistant behavior pack or TeamFoundry-inspired example, but APP should not become a persona marketplace.

### 4. APP-To-Engine Translation Layer

Define how APP concepts translate into engine-native artifacts. OpenClaw should be the first adapter target because it is the current proof-of-concept runtime and already uses Agent Skills-shaped skills.

Illustrative mappings:

```text
APP playbook -> runtime skill, prompt workflow, or executable behavior
APP scheduled behavior -> runtime habit, cron prompt, or scheduler integration
APP event response -> runtime hook, reflex, or event handler
APP contract -> workspace, report, data, or persistence convention
APP run manifest -> persisted execution record
```

The goal is not to make OpenClaw the required runtime. The goal is to learn from a concrete adapter while preserving APP's runtime neutrality.

### 5. TFY Assistant Construction Model

Reframe TeamFoundry assistant construction around modular inputs:

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

This model lets TeamFoundry cultivate high-quality assistant input content while reducing direct coupling between reusable behavior and one runtime's inventory format.

### 6. Pack Store Versus TFY Storefront Boundary

Clarify the boundary between reusable behavior distribution and human-facing assistant commerce or service.

APP Pack Store:

- Discovers reusable behavior packs
- Validates manifests and skill dependencies
- Publishes compatibility and trust metadata
- Supports public, private, or enterprise catalogs

TeamFoundry storefront:

- Presents assistants to humans
- Selects or assembles assistant offerings
- Handles onboarding and relationship setup
- Operates deployed assistant instances
- Shields customers from AI infrastructure details

### 7. Pilot Migration

Use one concrete TeamFoundry behavior as a proving ground. Candidate pilots include:

- TeamFoundry Employee base behavior
- Warren or another investment-advisor assistant behavior
- Portfolio analysis or market report behavior
- HQ request intake behavior

The pilot should test whether APP can represent the reusable behavior cleanly and whether TeamFoundry can translate it into an engine-specific assistant instance without collapsing APP and TFY into one project.

### 8. Wind-Down Of Multi-Repo Mode

Define an explicit exit from the temporary shared working context. Multi-repo exploration should taper off when:

- APP has stable enough concepts for packs, playbooks, overlays, skills, contracts, manifests, and adapter profiles.
- TeamFoundry has documented how it consumes APP packs as assistant construction input.
- OpenClaw-specific assumptions are isolated behind adapter language.
- At least one pilot behavior has clarified what belongs in APP, what belongs in TFY, and what belongs in the engine.
- Future changes can proceed through normal repo-local work and versioned contracts.

## Pilot Selection Criteria

The first pilot should be small enough to complete, rich enough to expose the boundary, and familiar enough to validate against existing TeamFoundry behavior.

A good pilot should include:

- One clear user or operator intent
- At least one Agent Skill-shaped capability
- At least one gate or confirmation step
- One durable output or run record
- One engine-specific translation question
- A clear decision about what remains TeamFoundry-owned

The pilot should not attempt a complete TeamFoundry migration. It should prove or falsify the APP translation-layer hypothesis.

## Non-Goals

This realignment does not require APP to become:

- A replacement for Agent Skills
- A replacement for TeamFoundry
- A replacement for OpenClaw
- A runtime orchestration engine
- A deployment or permission system
- A permanent control repository for TeamFoundry
- A persona marketplace by itself

This realignment does not require TeamFoundry to abandon OpenClaw. OpenClaw remains the practical first runtime target. The strategic shift is to stop treating OpenClaw-shaped artifacts as the long-term source format for all reusable assistant behavior.

## Desired End State

The desired end state is a cleaner stack:

- Humans interact with assistants.
- TeamFoundry offers, constructs, deploys, and operates those assistants.
- APP packages reusable assistant behaviors and domain playbooks.
- Agent Skills package granular capabilities.
- Agent engines execute through adapters.
- Tools, MCP, APIs, and channels provide concrete action and integration surfaces.

In that end state, TeamFoundry can continue to benefit from OpenClaw while becoming less conceptually coupled to it. APP can mature as a portable behavior-pack framework without becoming a TeamFoundry-specific implementation repo. The shared workbench phase ends once the boundary is clear enough for each project to evolve independently.
