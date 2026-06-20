# TeamFoundry Stack Realignment

This folder contains documentation for the temporary APP and TeamFoundry stack realignment program.

For current phase, priorities, pilot status, and decisions, read `teamfoundry-stack-realignment-plan.md`. That plan document is the only place program status should be tracked or updated.

## Read Order

1. `teamfoundry-stack-realignment-vision.md` — baseline strategic thesis; stable after acceptance
2. `teamfoundry-stack-realignment-plan.md` — status, work patterns, pillars, decision log
3. `app-design.md` — current APP design
4. `tfy-design.md` — current TeamFoundry design, translation flow, simulator model

When the vision and plan disagree on implementation details, follow the plan decision log and the current design documents.

## Document Roles

| Document | Role | Update frequency |
| --- | --- | --- |
| Vision | Why the realignment exists; initial stack model and roadmap pillars | Rarely; baseline only |
| Plan | Status, coordination, work patterns, decisions, next actions | Frequently |
| APP design | Current APP-owned behavior contract model | As design changes |
| TFY design | Current TeamFoundry-owned consumption, assembly, translation, simulator model | As design changes |
| This README | How to use this folder | Infrequently |

Design documents are current-state only. They do not narrate history. Meaningful pivots belong in the plan decision log.

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

| Path | Use for |
| --- | --- |
| `docs/framework.md` | Core APP concepts and layer model |
| `docs/agent-skills-integration.md` | Agent Skills compatibility |
| `docs/naming.md` | APP naming and ASP pivot context |
| `schema/app-manifest-v0.1.md` | Draft manifest shape |
| `examples/trading-coach-mini/` | Miniature APP pack example |
| `examples/teamfoundry-employee-base/` | TFY realignment pilot example and design sketch |

Example READMEs describe pack intent and design. They are not status trackers. Check the plan document for what exists on disk and what to do next.

## Implementation Artifact Locations

| Artifact | Location |
| --- | --- |
| TFY-derived APP examples | `examples/` |
| Local TFY simulator | `tools/tfy-simulator/` |
| Simulator preview output | `tools/tfy-simulator/output/` |
| Stable APP framework docs | `docs/`, `schema/`, `examples/` after graduation from design docs |

## How To Use This Folder

- Read the plan before starting work.
- Use design documents for current APP or TFY design boundaries.
- Use example directories for pack design reference; verify file existence on disk or in the plan before assuming materialization.
- Record status, decisions, and next actions only in the plan document.
