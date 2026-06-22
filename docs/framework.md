# APP Framework Baseline

## Working Name

AgentPlaybookPack, abbreviated APP.

The name is provisional, but the intent is clear: avoid competing with Agent Skills by making the playbook pack the primary unit of composition.

## Definition

An AgentPlaybookPack is a portable, runtime-neutral package for domain workflows that agents can discover, interpret, and execute.

It describes:

- What user intents the pack supports
- Which inputs must be resolved
- Which skills and tools are used
- Which workflow gates must clear
- Which overlays may augment the core output
- Which artifacts are produced
- How the run is recorded

## Design Goals

1. Fit into existing interchange work instead of duplicating it.
2. Treat agentskills.io as the preferred skill packaging format.
3. Keep the pack understandable without a specific runtime.
4. Make natural-language invocation first class.
5. Separate core output from optional augmentation.
6. Support durable artifacts, run manifests, and immutable history where useful.
7. Allow engine-specific implementations without making them the source of truth.

## Non Goals

APP is not:

- A replacement for Agent Skills
- A replacement for MCP
- A runtime orchestration engine
- A tool permission model
- A monolithic agent application framework

## Core Concepts

| Term | Meaning |
| --- | --- |
| Pack | A domain package containing playbooks, skills, workflows, overlays, contracts, and manifests |
| Playbook | A user-intent workflow, such as "review my portfolio" or "plan my trip" |
| Skill | A granular capability, preferably packaged using agentskills.io |
| Workflow | Shared lifecycle infrastructure, such as input discovery, context assembly, validation, and scope confirmation |
| Overlay | Optional augmentation of a playbook, such as evaluation, advisory, policy, enrichment, or presentation |
| Contract | Durable data, artifact, governance, or persistence rule |
| Manifest | Structured metadata describing composition, inputs, gates, outputs, and versioning |
| Run Manifest | A record of one completed execution |

## Layer Model

```text
Layer 3  Playbooks
  User-intent workflows. They compose skills, workflows, contracts, and overlays.
  Pack folder: layer3-playbooks/

Layer 2  Overlays
  Optional augmentations. They modify output or process without changing the core intent.
  Pack folder: layer2-overlays/ (pack-level); layer3-playbooks/<id>/overlays/ (playbook-scoped)

Layer 1  Skills
  Granular capability units. APP should prefer agentskills.io-compatible directories.
  Pack folder: layer1-skills/

Layer 0  Workflows
  Reusable execution infrastructure: discovery, input resolution, gates, validation, scope.
  Pack folder: layer0-workflows/
```

Cross-cutting pack folders `contracts/` and `gates/` are not layer-numbered. Each pack lives in a self-contained `{packId}.app/` folder. APP distribution repos contain only `README.md` and `*.app/` at repo root.

**Execution agents:** read [`app-execution.md`](app-execution.md) and each pack's `APP-EXECUTION.md`. **Skills:** true agentskills.io directories per [`app-skills.md`](app-skills.md).

The pack may also describe tool requirements, but tool implementations belong to runtimes or tool protocols such as MCP.

## Invocation Model

Users invoke playbooks in natural language. At the platform boundary, execution requires an APP repo address, a directive (pack + playbook or intent), and optional partial inputs; the executing agent mediates missing parameters.

The agent or runtime should:

1. Detect the relevant pack.
2. Select the playbook.
3. Resolve playbook inputs.
4. Activate required skills.
5. Clear workflow gates.
6. Apply optional overlays.
7. Produce the configured output artifacts.
8. Write a run manifest when the pack requires one.

## Discovery, Execution, Factory

APP keeps three modes distinct:

- Discovery: answer what the pack can do.
- Execution: run a playbook after user intent is clear.
- Factory: modify the pack itself.

This distinction prevents simple catalog questions from triggering data reads, handshakes, tool calls, or report generation.

## Core vs Augmented Output

Playbooks should define a core output that can run without optional overlays.

Overlays can add:

- Evaluation
- Advice
- Enrichment
- Policy checks
- Presentation variants
- Personalization

This keeps factual workflows reusable while allowing richer product behavior when requested.
