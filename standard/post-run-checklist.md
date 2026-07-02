# APP Post-Run Checklist v0.1

Contract-driven self-verification for execution agents after primary outputs are written. Complete this checklist before considering a run closed. APP does not enforce the checklist automatically — the agent attests results in the run summary or report appendix.

Operational context: [`app-execution.md`](app-execution.md).

---

## How to use

1. Resolve the playbook's `outputs.primary.contract` (and any secondary contracts referenced by overlays or workflows).
2. Walk each section below; mark pass, fail, or not-applicable.
3. On fail: document the gap in the report appendix or run summary; do not claim the run is complete.

---

## Checklist

### Bindings and inputs

| # | Check | Source |
| --- | --- | --- |
| B1 | `{userDatastore}` was bound before any durable write | [`app-execution.md`](app-execution.md) |
| B2 | Playbook inputs resolved per layer 0 workflow and manifest defaults | Playbook manifest `inputs:`, `defaultResolution:` |
| B3 | **Inputs Resolved** block present when the output contract requires it | Output contract |

### Gates

| # | Check | Source |
| --- | --- | --- |
| G1 | Every required gate on the playbook manifest was cleared | `<playbook-id>.app.yaml` `gates:` |
| G2 | Minimum evidence recorded for each cleared gate (see [`app-authoring.md`](app-authoring.md#gates-and-evidence)) | Workflow or skill that clears the gate |
| G3 | Conditional gates (`when:`) skipped or cleared per resolved inputs | Playbook manifest |

### Skills and overlays

| # | Check | Source |
| --- | --- | --- |
| S1 | Each `uses:` skill ran per its `SKILL.md` Procedure | Playbook manifest |
| S2 | Bundled scripts invoked with `--datastore` / `--workspace` (or documented equivalent) when Scripts section requires | Skill `SKILL.md` |
| S3 | `scaffold` skills: agent filled narrative sections the script did not produce | Skill `outputCompleteness` |
| O1 | Overlays with matching `when:` applied; others omitted | Playbook manifest `overlays:` |

### Primary output

| # | Check | Source |
| --- | --- | --- |
| P1 | Report folder exists at path resolved from `outputs.primary.pathTemplate` | Playbook manifest |
| P2 | Path tokens substituted correctly (`{userDatastore}`, `{timestamp}`, playbook report id) | Playbook manifest, output contract |
| P3 | All **required artifacts** listed in the output contract exist on disk | Output contract |
| P4 | Report sections meet contract minimums (including overlay-conditional sections) | Output contract |
| P5 | Timestamps are actual generation time — no placeholders | Output contract |
| P6 | No overwrite of an existing report folder (new timestamp if collision) | Output contract |

### Datastore layout

| # | Check | Source |
| --- | --- | --- |
| D1 | Writes under `{userDatastore}` conform to layout contract when `pack.app.yaml` references one | `contracts/user-datastore-layout.md` or pack equivalent |
| D2 | Mismatches between contract paths and on-disk layout documented in the report | [`app-execution.md`](app-execution.md) |

### Workspace

| # | Check | Source |
| --- | --- | --- |
| W1 | Intermediate skill outputs written under ephemeral `{agentWorkspace}`, not mixed into `{userDatastore}` except contract-required deliverables | [`app-execution.md`](app-execution.md) |
| W2 | Ephemeral workspace for this run removed after verification passes (unless user requested retention or run failed) | [`app-execution.md`](app-execution.md) |

---

## Attestation

Record in the run summary or report appendix:

```text
Post-run checklist: <passed | failed>
Failed items: <ids or "none">
Notes: <optional>
```
