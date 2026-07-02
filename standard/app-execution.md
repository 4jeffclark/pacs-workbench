# APP Execution Guide v0.1

Operational guide for **execution agents** running APP packs. Normative format rules live in [`app-authoring.md`](app-authoring.md). This document defines how to **open** and **close** a run with the same rigor authors expect when writing packs.

APP is **fire-and-forget**: read instructions, execute, write primary outputs, self-verify, done. APP does not orchestrate, track runs, or stay involved afterward.

Pack `README.md` is lightweight user documentation. It is not authoritative for execution.

---

## Read order

| Step | Read | Purpose |
| --- | --- | --- |
| 1 | [`app-authoring.md`](app-authoring.md) | Format grammar — layers, manifests, contracts, outcomes |
| 2 | This file | Operational steps — refresh, bind, execute, verify |
| 3 | [`pre-run-checklist.md`](pre-run-checklist.md) | Pre-run refresh verification — workbench and pack updates before execution |
| 4 | Distribution repo `README.md` | Pack index (optional human context) |
| 5 | `{packId}.app/pack.app.yaml` | Bind pack inputs; discover playbooks |
| 6 | `layer3-playbooks/<id>/<id>.app.yaml` | Resolve playbook inputs, composition, gates, outputs |
| 7 | Manifest-referenced artifacts only | Workflows, skills, overlays, contracts |

Do not crawl the full pack tree. Do not treat workbench `documentation/examples/` as an execution target unless explicitly directed — use a **distribution repo**.

---

## Modes and handoff

| Mode | Outcome |
| --- | --- |
| **Discovery** | Answer what the pack can do. Do not bind `{userDatastore}`, read user data, or write reports. |
| **Execution** | Run a playbook after user intent is clear. |
| **Factory** | Modify the pack itself (authoring context only). |

**Discovery → execution handoff:** When discovery and execution occur in the same session, stop discovery before binding `{userDatastore}`. Confirm the target playbook, bindings, and resolved inputs (or declared defaults) before any workflow runs. Discovery must not write durable outputs under `{userDatastore}`.

---

## Pack provisioning (recommended)

The standard defines pack **shape**, not how an engine obtains a pack. Use this convention unless the run request specifies otherwise:

| Field | Meaning |
| --- | --- |
| `distributionUrl` | Git or HTTP URL of the distribution repo |
| `ref` | Commit, tag, or branch to pin (recommended for reproducibility) |
| `packInstance` | Path to `{packId}.app/` inside the repo |
| `playbookId` | Playbook `id` from `pack.app.yaml` `playbooks:` |

Example intent: *Run `hello-world` from `hello-world-app` at ref `v1.0.0`, pack instance `hello-world.app/`, user datastore `UserData/alice`.*

How the engine clones, vendors, or caches the repo is **platform scope** — not APP standard. Hosts may run refresh before the agent session starts; when they do, the agent still attests per [Pre-run verification](#pre-run-verification).

---

## Pre-run refresh

Before reading pack manifests or binding `{userDatastore}` for **execution**, refresh two sources:

| Source | Contents | When local copy exists | When no local copy yet |
| --- | --- | --- | --- |
| **Workbench standard** | `app-authoring.md`, `app-execution.md`, checklists | `git fetch`; compare HEAD to remote; `git pull` when not pinned and behind | Fetch canonical URLs or clone workbench at requested ref |
| **Distribution pack** | `{packId}.app/` behavior in the product repo | `git fetch`; compare HEAD to remote; `git pull` or re-clone when not pinned and behind | Clone at pinned `ref` or latest default branch during [Provision](#execution-sequence) |

### Pinning

| Run request | Behavior |
| --- | --- |
| Pinned `ref` (commit, tag, branch) | Verify local copy matches pin; do **not** pull a newer version |
| **Latest** or no `ref` | Fetch remote and update local copy before manifest reads |
| Discovery-only (no execution handoff) | Pack refresh optional; workbench refresh recommended when using a local clone |

Record resolved refs and `pack.app.yaml` `version` in [pre-run attestation](pre-run-checklist.md#attestation).

Packs may add optional `layer0-workflows/pack-sync.md` for repo-specific sync steps (private remotes, multi-repo skills). Complete it when referenced from the pack or playbook manifest, after generic refresh above.

Platform hosts (CI, Cursor hooks, custom runners) may perform refresh before the agent runs. That does not replace agent attestation — record what the host synced or confirm local state matches remote.

---

## Bindings

Before core execution:

| Input | Role |
| --- | --- |
| `{userDatastore}` | User persistent storage (reports, raw data, inputs) |
| `{agentWorkspace}` | Ephemeral temp and intermediate artifacts for this run |

`{userDatastore}` is always bound when a playbook reads or writes user data. Neither binding lives in the APP behavior repo.

### `{agentWorkspace}` — when the user is silent

`agentWorkspace` is an **optional** pack input (see [`app-authoring.md`](app-authoring.md)). When the user or platform does not supply it, the execution agent **chooses** an ephemeral workspace for the run.

Outcomes:

- Intermediates stay out of `{userDatastore}` except contract-required deliverables.
- The user-facing experience is deliverables under `{userDatastore}` — not scratch files left in visible project roots.
- After post-run verification passes, **remove the ephemeral workspace** for that run (or its run-scoped subdirectory). Retain only when debugging a failed run or when the user asked to keep artifacts.

Platform hosts with project-scoped guardrails (e.g. Cursor) may use a hidden project folder such as `.tmp/` for ephemeral workspace and pack provisioning. That choice is platform scope; APP does not mandate a folder name.

When the user **does** supply `{agentWorkspace}`, use that path — typically because storage must be coordinated with the user or host policy.

### Run isolation (platform scope)

Hosts may isolate concurrent runs with per-run subdirectories (e.g. `<workspace>/<timestamp>-<playbookReportId>/`). APP does not prescribe internal layout; pass the active directory as `--workspace` to skill scripts.

---

## Execution sequence

Given a pack instance address and resolved playbook:

1. **Refresh** — update workbench standard and distribution pack to latest (unless pinned); complete the [pre-run checklist](pre-run-checklist.md).
2. **Provision** — obtain the distribution repo when no suitable local copy exists (see [Pack provisioning](#pack-provisioning-recommended)).
3. **Read manifests** — `pack.app.yaml` → `<playbook-id>.app.yaml` → referenced artifacts only.
4. **Bind** — set `{userDatastore}`; set or select ephemeral `{agentWorkspace}` (see above).
5. **Resolve inputs** — run required layer 0 workflows (typically `input-discovery`). Apply manifest `default` values and playbook `defaultResolution` policies when the user did not specify a value (see [`app-authoring.md`](app-authoring.md#default-resolution-policies)).
6. **Clear gates** — complete workflows and skills; record minimum evidence per gate (see [`app-authoring.md`](app-authoring.md#gates-and-evidence)).
7. **Run skills** — execute per each `SKILL.md` Procedure; run bundled scripts only when instructed.
8. **Apply overlays** — when manifest `when:` conditions match resolved inputs.
9. **Write outputs** — primary report and contract-required artifacts under `{userDatastore}` per playbook manifest and output contracts.
10. **Self-verify** — complete the [post-run checklist](post-run-checklist.md) against referenced contracts.

### Rules

- Prompt-first; run bundled scripts only when `SKILL.md` instructs.
- No ad-hoc scripts during a run.
- Core output runs without optional overlays unless playbook inputs enable them.
- When contracts and on-disk layout disagree, trust raw files and document the mismatch in the report.

---

## Script invocation

Bundled skill scripts must accept explicit paths as the canonical interface:

```text
--datastore <path>    bound {userDatastore}
--workspace <path>    bound {agentWorkspace} or active run subdirectory
```

Shell environment variables (`$USER_DATASTORE`, `$AGENT_WORKSPACE`) are optional ergonomics. Prefer the flags above for cross-platform execution.

**Cross-platform examples** (equivalent invocations):

```bash
# Unix shell
python scripts/run.py --recipient "Alice" --workspace "$AGENT_WORKSPACE"
```

```powershell
# PowerShell
python scripts/run.py --recipient "Alice" --workspace $env:AGENT_WORKSPACE
```

Authors document both forms or the flag form only in each skill's **Scripts** section.

---

## Skill output expectations

Skills declare outputs in `SKILL.md`. Optional frontmatter `outputCompleteness` tells the agent how much synthesis is required:

| Value | Meaning |
| --- | --- |
| `complete` | Script or procedure produces final artifact content; agent assembles only |
| `scaffold` | Script produces structure or indexes; agent fills narrative per Procedure |

When omitted, treat outputs as `complete` if a bundled script produces them; otherwise infer from the Procedure.

---

## Pre-run verification

Before reading manifests or binding `{userDatastore}` for execution, self-verify using [`pre-run-checklist.md`](pre-run-checklist.md). Failed checks must be reported in the run summary; do not proceed to playbook execution until refresh passes or the user accepts a pinned stale ref.

---

## Post-run verification

After primary outputs are written, self-verify using [`post-run-checklist.md`](post-run-checklist.md). The checklist is contract-driven — not a separate orchestrator. Failed checks must be reported in the run summary or report appendix.

Gate clearance remains self-attested unless a pack contract defines machine-checkable evidence artifacts.

---

## Validation tooling

`validate-manifests.py` is for **pack authors and CI** only. Execution agents do not run it before executing a distribution pack unless an explicit run request or pack README says otherwise.

---

## Version

APP execution guide v0.1. Pairs with APP authoring standard v0.1.
