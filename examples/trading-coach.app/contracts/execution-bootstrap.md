# Agent Bootstrap (legacy ASP)

> **Superseded by [`APP-EXECUTION.md`](../APP-EXECUTION.md)** at the pack instance root. Retained for migration reference only.

## Modes

| Mode | When | Read first |
|---|---|---|
| **Discovery** | User asks what is available, what playbooks exist, or what you can do | [README.md](../README.md) → [layer3-playbooks/README.md](../playbooks/README.md) |
| **Execution** | User expresses run intent (analysis, review, profile, post-mortem) | [PROJECT.md](../PROJECT.md) → [AGENT_GIT_PROTOCOL.md](../AGENT_GIT_PROTOCOL.md) → [contracts/datastore-contract.md](../contracts/datastore-contract.md) → `layer3-playbooks/<id>/` |
| **Factory** | User asks to extend playbooks, capabilities, workflows, contracts, or repo structure | [DEVELOPMENT.md](../DEVELOPMENT.md) → [AGENTS.md](../AGENTS.md) → [PROJECT.md](../PROJECT.md) |

## Discovery rules

- Answer catalog questions from **README.md** (*What you can ask for*) and **layer3-playbooks/README.md**.
- Map natural language to playbook id + lenses per [agent-layer-integration.md](agent-layer-integration.md).
- Do **not** emit the TradingCoach Framework handshake until run intent is clear.
- Do **not** read `contracts/datastore-contract.md` or ingest data during discovery-only turns.

## Execution rules

- Emit the **TradingCoach Framework** handshake on first response after run intent (see [AGENTS.md](../AGENTS.md)).
- Resolve inputs via **Structured Inputs Framework** in `PROJECT.md`; present **Inputs Resolved**.
- New report folders use **timestamp-first PlaybookReportId** naming (see [contracts/report-artifact-contract.md](../contracts/report-artifact-contract.md)).
- **`GenerationTimestamp`** must be actual wall-clock time at folder creation; never placeholders; never overwrite an existing folder.
- Path: `{userDatastore}/reports/<GenerationTimestamp>-<PlaybookReportId>-<AnalysisStart>-<AnalysisEnd>/`
- Populate `Manifest.md` with ASP fields including `Output Mode` and typed capability/overlay execution lists.
- **`Report.md` must be self-contained** per `PROJECT.md` **Report Self-Containment Contract** (full Appendix C citations; no sibling file pointers).
- Apply **Report.md Rendering Conventions**: GitHub-safe Mermaid only; markdown table fallback for every figure.
- Reports are immutable after finalization.

## Prompt-first execution

Follow skill procedures in `SKILL.md`. Use **bundled scripts** under `layer1-skills/<id>/scripts/` when `SKILL.md` instructs it (agentskills.io). Do **not** invent ad-hoc analysis scripts during playbook runs.

## Do not read by default

| Path | Reason |
|---|---|
| `reference/archives/` | Archived POC; not part of default execution |
| `DEVELOPMENT.md` | Factory mode only |
| `docs/asp-validation-suite.md` | Internal validation checklist |
| Prior `{userDatastore}/reports/` folders | Unless user supplies one as source context |
