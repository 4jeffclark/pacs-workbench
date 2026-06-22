# Workflow — structured-input-discovery

## Workflow Id

`structured-input-discovery`

## Layer

0 — infrastructure

## Purpose

Parse playbook **Inputs** from natural language and attachments; present **Inputs Resolved**; reconcile pending parameters.

## Procedure

Follow **Structured Inputs Framework** in [PROJECT.md](../PROJECT.md):

1. **Parse** — infer all declared Inputs from user request, attachments, repository context
2. **Summarize** — present **Inputs Resolved** with every parameter (`confirmed`, `proposed default`, or `pending`)
3. **Reconcile** — ask plain-language questions for pending/ambiguous parameters only
4. **Confirm** — update summary after each reconciliation turn

Users do not need fixed parameter syntax (e.g. `evaluation: false`).

## Outputs

- Final **Inputs Resolved** block
- Reconciliation transcript (embedded in report Appendix A when `evaluation: false`)

## Manifest

See [structured-input-discovery.asp.yaml](structured-input-discovery.asp.yaml)
