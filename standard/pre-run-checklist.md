# APP Pre-Run Checklist v0.1

Contract-driven self-verification for execution agents **before** reading pack manifests or running a playbook. Complete this checklist when entering **execution** mode (and when discovery may hand off to execution in the same session). APP does not enforce the checklist automatically — the agent attests results in the run summary or report appendix.

Operational context: [`app-execution.md`](app-execution.md).

---

## How to use

1. Resolve the run request: distribution repo, optional pinned `ref`, pack instance, playbook id, and `{userDatastore}`.
2. Refresh the workbench standard and distribution pack per object [Pinning](#pinning) applies.
3. Walk each section below; mark pass, fail, skipped-pinned, or not-applicable.
4. On fail: do not proceed to manifest reads or playbook execution until refresh succeeds or the user accepts a pinned stale ref.

**Discovery-only sessions** that will not bind `{userDatastore}` or run workflows may skip pack refresh; still refresh the workbench standard when a local clone is used.

---

## Pinning

When the run request specifies a pinned `ref` (commit, tag, or branch) for the distribution repo or workbench standard, **do not** pull a newer version. Verify the local copy matches the pin and record `skipped-pinned` in attestation.

When the user asks for **latest** or does not specify a `ref`, fetch from remote and update the local copy before execution.

---

## Checklist

### Workbench standard

| # | Check | Source |
| --- | --- | --- |
| W0 | Workbench standard source identified (local clone path or canonical URL) | [`app-execution.md`](app-execution.md#pre-run-refresh) |
| W1 | `app-authoring.md`, `app-execution.md`, `pre-run-checklist.md`, and `post-run-checklist.md` are at the requested ref | Workbench `standard/` or fetched URLs |
| W2 | When not pinned: workbench remote fetched and local HEAD matches remote default branch (or user-specified tracking branch) | Git or platform sync |
| W3 | When pinned: local workbench ref matches the pin | Run request |

### Distribution pack

| # | Check | Source |
| --- | --- | --- |
| P0 | Distribution repo identified (`distributionUrl` or local path) | Run request, pack `README.md`, or user |
| P1 | When not pinned: remote fetched and local copy updated to latest default branch (or user-specified branch) before manifest reads | Git or platform sync |
| P2 | When pinned: local distribution ref matches the pin | Run request |
| P3 | `pack.app.yaml` `version` field recorded for this run | `{packId}.app/pack.app.yaml` |
| P4 | Target playbook id listed in `pack.app.yaml` `playbooks:` | Pack manifest |

### Optional pack workflow

| # | Check | Source |
| --- | --- | --- |
| O0 | When the pack defines `layer0-workflows/pack-sync.md` and the playbook or pack manifest references it: pack-specific sync steps completed | Pack layer 0 workflow |

---

## Attestation

Record in the run summary before reading manifests or binding `{userDatastore}`:

```text
Pre-run refresh: <passed | skipped-pinned | failed | not-applicable>
Workbench ref: <commit, tag, or URL@ref>
Distribution ref: <commit or tag>
Pack version: <from pack.app.yaml>
Failed items: <ids or "none">
Notes: <optional — e.g. updated from abc123 to def456>
```

When `Pre-run refresh` is `failed`, do not claim execution has started.
