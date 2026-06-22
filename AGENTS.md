# AgentPlaybookPack Agent Guide

## APP Standards (any task)

Start here for normative APP work:

1. `docs/README.md` — standards index
2. `docs/framework.md` — concepts and layer model
3. `docs/app-execution.md` — execution agent guide
4. `schema/app-manifest-v0.1.md` — manifest draft
5. `examples/trading-coach.app/` — reference materialized instance

Sketches in `sketches/` are non-published and may not follow current conventions.

## Active Work

The current priority is the TeamFoundry stack realalignment program.

Start here: `docs/tfy-stack-realignment/README.md`

Read order:

1. `docs/tfy-stack-realignment/teamfoundry-stack-realignment-vision.md`
2. `docs/tfy-stack-realignment/teamfoundry-stack-realignment-plan.md`
3. `docs/tfy-stack-realignment/app-design.md`
4. `docs/tfy-stack-realignment/tfy-design.md`

All program status, pilot materialization state, and next actions live in the plan document.

## Work Rules

- Use `agent-playbook-pack` as the active workspace.
- Treat `teamfoundry.ai` as read-only during early realignment work.
- Follow accepted design decisions in the plan design decision log when vision and current design differ.
- Do not rewrite the vision document to track later pivots.
- Update the plan design decision log for meaningful architecture and product-design decisions.
- Update `app-design.md` or `tfy-design.md` for accepted current design changes.
- Do not add status tracking to README files; update the plan instead.
- Use Sketch-Then-Materialize: do not create whole example trees unless explicitly requested.

## Key References

- APP standards index: `docs/README.md`
- APP framework: `docs/framework.md`
- APP execution guide: `docs/app-execution.md`
- APP manifest draft: `schema/app-manifest-v0.1.md`
- Simulator design and location: `docs/tfy-stack-realignment/tfy-design.md`, `tools/tfy-simulator/`
- Pilot example: `examples/trading-coach.app/` (APP distribution repo: `examples/`)
- Deferred sketch: `sketches/teamfoundry-employee-base/README.md`

## Agent Test Tasks

Use these in a fresh Cursor thread to validate repo bootstrap:

1. Summarize the realignment effort and current phase without chat history.
2. Run the task in the plan `Current Focus` section.
3. Propose the next single file to materialize for the accepted pilot and explain why.
