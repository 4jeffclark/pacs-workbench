# TeamFoundry Stack Realignment

This folder is the active program workspace for aligning APP and TeamFoundry during a temporary multi-repo realignment phase.

## Start Here

Read in this order:

1. `teamfoundry-stack-realignment-vision.md` — baseline strategic thesis; stable after acceptance
2. `teamfoundry-stack-realignment-plan.md` — current focus, work patterns, pillars, decision log
3. `app-design.md` — current APP design for the shared behavior contract
4. `tfy-design.md` — current TeamFoundry design, translation flow, simulator model

When the vision and plan disagree on implementation details, follow the plan decision log and the current design documents.

## Document Roles

| Document | Role |
| --- | --- |
| Vision | Why the realignment exists; initial stack model and roadmap pillars |
| Plan | Shared coordination, status, work patterns, decisions, next actions |
| APP design | Current APP-owned behavior contract model |
| TFY design | Current TeamFoundry-owned consumption, assembly, translation, simulator model |

Design documents are current-state only. They do not narrate history. Meaningful pivots belong in the plan decision log.

## Current Phase

```text
Phase: Baseline Pillar 1 and prepare first pilot
Active repo: agent-playbook-pack
Reference repo: teamfoundry.ai (read-only)
Optional reference: openclaw (runtime mechanics only)
Do not edit: teamfoundry.ai during early APP exploration
```

## Adjacent Repositories

Side-by-side clones on the same workstation:

```text
C:\code\agent-playbook-pack
C:\code\teamfoundry.ai
C:\code\openclaw
```

This is a temporary working-context assumption, not a monorepo, submodule layout, or permanent dependency relationship.

## TeamFoundry Reference Map

Use these entry points when reading `teamfoundry.ai`:

| Path | Use for |
| --- | --- |
| `docs/TeamFoundry-Product-Documentation.md` | Foundry, Forge, HQ model |
| `foundry/ops/inventories/skills/` | Agent Skills-shaped TFY skills |
| `foundry/ops/casts/` | Base casts such as `teamfoundry-employee` |
| `forge/ops/agents-forged/Warren/` | Forged assistant example |
| `forge/ops/agents-forged/Warren/inventories/habits/` | Scheduled behavior examples |
| `foundry/ops/inventories/skills/hq-requests/` | HQ request intake behavior |

## APP Framework References

During this realignment, treat these as the durable APP framework references unless superseded by an accepted decision and updated design doc:

| Path | Use for |
| --- | --- |
| `docs/framework.md` | Core APP concepts and layer model |
| `docs/agent-skills-integration.md` | Agent Skills compatibility |
| `docs/naming.md` | APP naming and ASP pivot context |
| `schema/app-manifest-v0.1.md` | Draft manifest shape |
| `examples/trading-coach-mini/` | Miniature APP pack example |

Realignment-specific design lives in `app-design.md` and may evolve ahead of the general framework docs during pilots.

## Work Rules For Development Agents

- Treat `agent-playbook-pack` as the implementation workspace.
- Read from `teamfoundry.ai`; do not edit it during early realignment work.
- Use pilot-first, adapter-last, and two-step TFY implementation patterns from the plan.
- Update the plan decision log for meaningful architecture decisions.
- Update `app-design.md` or `tfy-design.md` to reflect accepted current design.
- Do not rewrite the vision document to track later pivots.
- Do not treat OpenClaw-shaped inventory as the APP source-of-truth format.
- Do not build TFY integration in the TFY repo until APP representations and simulator validation are credible.

## Implementation Artifact Locations

| Artifact | Intended location |
| --- | --- |
| TFY-derived APP examples | `examples/` |
| Local TFY simulator | `tools/tfy-simulator/` |
| Simulator preview output | `tools/tfy-simulator/output/` |
| Stable APP framework docs | `docs/`, `schema/`, `examples/` after graduation from design docs |

## Accepted Model Reminder

Translation is TeamFoundry-owned through assistant assembly context. APP expresses portable behavior intent. TeamFoundry ingests APP packs, assembles assistant inputs, and translates to HQ-deployable, engine-specific artifacts. See the 2026-06-20 decision log entry in the plan document.
