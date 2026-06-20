# AgentPlaybookPack Agent Guide

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
- Follow accepted decisions in the plan decision log when vision and current design differ.
- Do not rewrite the vision document to track later pivots.
- Update the plan decision log for meaningful architecture decisions.
- Update `app-design.md` or `tfy-design.md` for accepted current design changes.
- Do not add status tracking to README files; update the plan instead.
- Use Sketch-Then-Materialize: do not create whole example trees unless explicitly requested.

## Key References

- APP framework: `docs/framework.md`
- APP manifest draft: `schema/app-manifest-v0.1.md`
- Simulator design and location: `docs/tfy-stack-realignment/tfy-design.md`, `tools/tfy-simulator/`
- Pilot example design sketch: `examples/teamfoundry-employee-base/README.md`

## Agent Test Tasks

Use these in a fresh Cursor thread to validate repo bootstrap:

1. Summarize the realignment effort and current phase without chat history.
2. Run the task in the plan `Current Focus` section.
3. Propose the next single file to materialize for the accepted pilot and explain why.
