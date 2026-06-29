# Workflow — input-discovery

## Workflow Id

`input-discovery`

## Layer

0 — infrastructure

## Workflow kind

**Agent-only procedure** — no companion script. Minimum gate evidence: Procedure completed; **Inputs Resolved** block embedded in `Report.md` per output contract.

## Purpose

Resolve playbook inputs from natural language before core execution.

## Procedure

1. **Parse** — infer `recipient`, `friendly`, and `banner` from the user request and any supplied partial `inputs`
2. **Summarize** — present **Inputs Resolved** with each parameter marked `confirmed`, `default`, or `pending`
3. **Reconcile** — ask plain-language questions only for pending or ambiguous parameters
4. **Confirm** — finalize the input block before clearing the `inputs-resolved` gate (see `<playbook-id>.app.yaml`)

Users do not need fixed parameter syntax (for example `friendly: true`).

## Defaults

| Input | Default |
| --- | --- |
| `recipient` | `World` |
| `friendly` | `false` |
| `banner` | `false` |

## Outputs

- Final **Inputs Resolved** block (embed in report Appendix; see output contract template)
- Cleared `inputs-resolved` gate (self-attested)
