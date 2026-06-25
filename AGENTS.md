# AgentPlaybookPack Agent Guide

## APP Standards Workbench

This repo defines the APP format. It is **not** an APP distribution repo.

| Need | Read |
| --- | --- |
| Workbench map | [`README.md`](README.md) |
| Authoring standard (execution agents) | [`standard/app-authoring.md`](standard/app-authoring.md) |
| JSON Schemas and validator | [`standard/`](standard/) |
| Human product guide | [`documentation/app-workbench-guide.md`](documentation/app-workbench-guide.md) |
| Reference pack instances | [`examples/`](examples/) |

Execution agents learn APP from `standard/app-authoring.md`, then consume pack manifests and referenced layer artifacts. Pack `README.md` files are user welcome only.

## Work Rules

- Treat `standard/` as normative; when `standard/` and an example disagree, update the example.
- Validate manifests and layout: `python standard/validate-manifests.py` (schema + overlay paths, playbook index, forbidden legacy artifacts).
- Gate metadata lives on `<playbook-id>.app.yaml` only (no `gates/` folder).
- Pack shell entry is `pack.app.yaml` (no `APP-EXECUTION.md`).
- APP is fire-and-forget: behavioral instructions only; no run manifests or execution tracking.
- Use Sketch-Then-Materialize: do not create whole example trees unless explicitly requested.

## Key References

- Standard index: [`standard/README.md`](standard/README.md)
- Authoring standard: [`standard/app-authoring.md`](standard/app-authoring.md)
- Workbench guide: [`documentation/app-workbench-guide.md`](documentation/app-workbench-guide.md)
- hello-world reference: [`examples/hello-world.app/`](examples/hello-world.app/)
- portfolio-coach reference: [`examples/portfolio-coach.app/`](examples/portfolio-coach.app/)
