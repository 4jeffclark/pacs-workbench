# PACS Execution Guide v0.2

Operational guide for **execution agents** running PACS stacks. Normative format rules live in [`pacs-authoring.md`](pacs-authoring.md). This document defines how to **open** and **close** a run with the same rigor authors expect when writing packs.

PACS is **fire-and-forget**: read instructions, execute, write primary outputs, self-verify, done. PACS does not orchestrate, track runs, or stay involved afterward.

Pack `README.md` is lightweight user documentation. It is not authoritative for execution.

---

## Read order

| Step | Read | Purpose |
| --- | --- | --- |
| 1 | [`pacs-authoring.md`](pacs-authoring.md) | Format grammar — layers, manifests, contracts, outcomes |
| 2 | This file | Operational steps — refresh, bind, execute, verify |
| 3 | [`pre-run-checklist.md`](pre-run-checklist.md) | Pre-run refresh verification — workbench and pack updates before execution |
| 4 | Distribution repo `README.md` | Pack index (optional human context) |
| 5 | `{packId}.pacs/pack.pacs.yaml` | Bind pack inputs; discover playbooks |
| 6 | `layer3-playbooks/<id>/<id>.pacs.yaml` | Resolve playbook inputs, composition, gates, outputs |
| 7 | Manifest-referenced artifacts only | Workflows, skills, overlays, contracts |

Do not crawl the full pack tree. Do not treat workbench `documentation/examples/` as an execution target unless explicitly directed — use a **distribution repo**.

---

## Modes and handoff

| Mode | Outcome |
| --- | --- |
| **Discovery** | Answer what the pack can do. Do not bind `{userDatastore}`, read user data, or write reports. |
| **Execution** | Run a playbook after user intent is clear. Treat the provisioned distribution copy as read-only (see [Distribution repo boundary](#distribution-repo-boundary-execution-copy)). |
| **Factory** | Modify the pack in an authoring workspace; publish to the distribution remote — not in the execution cache. |

**Discovery → execution handoff:** When discovery and execution occur in the same session, stop discovery before binding `{userDatastore}`. Confirm the target playbook, bindings, and resolved inputs (or declared defaults) before any workflow runs. Discovery must not write durable outputs under `{userDatastore}`. At handoff, re-resolve inputs from the manifest and user run request — do not treat earlier discovery prose or visible prior deliverables as implicit inputs (see [Execution closure](#execution-closure-and-memory-planes)).

**Factory is not execution:** Factory modifies pack behavior in an **authoring workspace** (see [Distribution repo boundary](#distribution-repo-boundary-execution-copy)). Execution reads a provisioned copy only. Do not mix the two trees unless the user explicitly opts into a combined dev setup (see below).

---

## Distribution repo boundary (execution copy)

Execution agents consume distribution repos through a **one-way, read-only** relationship. The distribution remote is the published product; the local copy exists only to be refreshed and read during a run.

| Direction | Execution mode |
| --- | --- |
| Remote → local copy | **Yes** — `git fetch`, `git pull`, or re-clone per [Pre-run refresh](#pre-run-refresh) (unless pinned) |
| Local copy → remote | **Never** — do not commit, push, or open pull requests from the execution copy |
| Edits inside local copy | **Avoid** — treat the provisioned pack as immutable for the run |

### Durable writes belong elsewhere

During execution, durable outputs go to `{userDatastore}` (reports, user data) and ephemeral intermediates to `{agentWorkspace}`. The distribution repo and its local execution copy are **not** run output targets.

### Why read-only

Pre-run refresh replaces the local copy with the remote default branch (or pinned `ref`). Any edit under the execution copy is **lost on the next pull** and must not be treated as published pack behavior. Accidental commits from an execution workspace corrupt the separation between **running** a pack and **shipping** a pack.

### Factory vs execution workspace

| Role | Workspace | Git writes to distribution remote |
| --- | --- | --- |
| **Execution** | Provisioned execution copy (host-defined cache or fresh clone) | **Never** |
| **Factory** | Separate authoring clone or worktree (outside the execution cache) | **Yes** — authors commit and push here; execution agents pull the result |

Pack authors (humans or agents in Factory mode) change behavior only in the authoring workspace, publish to the distribution remote, then execution agents refresh their read-only copy before the next run.

### Platform provisioning

How the engine clones, vendors, or caches a distribution repo is **platform scope**. A host may keep execution copies under a dedicated folder (for example `packs/` in a test harness). That folder is an **execution cache**: pull to refresh, read manifests, invoke skills. It is not a substitute for an authoring workspace.

### Combined Factory + execution (explicit opt-in only)

Some development setups assign one agent both roles: run playbooks against `{userDatastore}` **and** assist with pack development. This is **not** the default PACS model.

When the user explicitly opts in:

1. **Factory** — edit, commit, and push only in the user-supplied **authoring clone** outside the execution workspace or execution cache.
2. **Execution** — run playbooks only against the refreshed execution copy; complete pre-run refresh before manifest reads.
3. **Handoff** — after Factory publishes to the distribution remote, refresh the execution copy (`git pull`) before the next execution run.

Even in combined setups: **never** commit or push pack changes from the execution workspace or execution cache.

---

## Pack provisioning (recommended)

The standard defines pack **shape**, not how an engine obtains a pack. Use this convention unless the run request specifies otherwise:

| Field | Meaning |
| --- | --- |
| `distributionUrl` | Git or HTTP URL of the distribution repo |
| `ref` | Commit, tag, or branch to pin (recommended for reproducibility) |
| `packInstance` | Path to `{packId}.pacs/` inside the repo |
| `playbookId` | Playbook `id` from `pack.pacs.yaml` `playbooks:` |

Example intent: *Run `hello-world` from `hello-world-pacs` at ref `v1.0.0`, pack instance `hello-world.pacs/`, user datastore `UserData/alice`.*

How the engine clones, vendors, or caches the repo is **platform scope** — not PACS standard. Hosts may run refresh before the agent session starts; when they do, the agent still attests per [Pre-run verification](#pre-run-verification).

---

## Pre-run refresh

Before reading pack manifests or binding `{userDatastore}` for **execution**, refresh two sources:

| Source | Contents | When local copy exists | When no local copy yet |
| --- | --- | --- | --- |
| **Workbench standard** | `pacs-authoring.md`, `pacs-execution.md`, checklists | `git fetch`; compare HEAD to remote; `git pull` when not pinned and behind | Fetch canonical URLs or clone workbench at requested ref |
| **Distribution pack** | `{packId}.pacs/` behavior in the product repo | `git fetch`; compare HEAD to remote; `git pull` or re-clone when not pinned and behind | Clone at pinned `ref` or latest default branch during [Provision](#execution-sequence) |

### Pinning

| Run request | Behavior |
| --- | --- |
| Pinned `ref` (commit, tag, branch) | Verify local copy matches pin; do **not** pull a newer version |
| **Latest** or no `ref` | Fetch remote and update local copy before manifest reads |
| Discovery-only (no execution handoff) | Pack refresh optional; workbench refresh recommended when using a local clone |

Record resolved refs and `pack.pacs.yaml` `version` in [pre-run attestation](pre-run-checklist.md#attestation).

Packs may add optional `layer0-workflows/pack-sync.md` for repo-specific sync steps (private remotes, multi-repo skills). Complete it when referenced from the pack or playbook manifest, after generic refresh above.

Platform hosts (CI, Cursor hooks, custom runners) may perform refresh before the agent runs. That does not replace agent attestation — record what the host synced or confirm local state matches remote.

---

## Bindings

Before core execution:

| Input | Role |
| --- | --- |
| `{userDatastore}` | User persistent storage (reports, raw data, inputs) |
| `{agentWorkspace}` | Ephemeral temp and intermediate artifacts for this run |

`{userDatastore}` is always bound when a playbook reads or writes user data. Neither binding lives in the PACS behavior repo.

### `{agentWorkspace}` — when the user is silent

`agentWorkspace` is an **optional** pack input (see [`pacs-authoring.md`](pacs-authoring.md)). When the user or platform does not supply it, the execution agent **chooses** an ephemeral workspace for the run.

Outcomes:

- Intermediates stay out of `{userDatastore}` except contract-required deliverables.
- The user-facing experience is deliverables under `{userDatastore}` — not scratch files left in visible project roots.
- After post-run verification passes, **remove the ephemeral workspace** for that run (or its run-scoped subdirectory). Retain only when debugging a failed run or when the user asked to keep artifacts.

Platform hosts with project-scoped guardrails (e.g. Cursor) may use a hidden project folder such as `.tmp/` for ephemeral workspace and pack provisioning. That choice is platform scope; PACS does not mandate a folder name.

When the user **does** supply `{agentWorkspace}`, use that path — typically because storage must be coordinated with the user or host policy.

### Run isolation (platform scope)

Hosts may isolate concurrent runs with per-run subdirectories (e.g. `<workspace>/<timestamp>-<playbookReportId>/`). PACS does not prescribe internal layout; pass the active directory as `--workspace` to skill scripts.

---

## Execution closure and memory planes

Execution agents operate in environments with **ambient context**: chat history, indexed workspace files, prior run artifacts, and platform rules. PACS treats ambient context as **non-authoritative** during execution unless explicitly promoted into the run's **closure set**.

### Memory planes

| Plane | Examples | Role during execution |
| --- | --- | --- |
| **Pack authority** | Workbench standard, distribution pack @ ref, manifest-referenced artifacts | Authoritative behavior |
| **Declared datastore** | Contract-defined raw, canonical, and knowledge paths; resolved playbook inputs | Authoritative inputs |
| **Ambient context** | Prior reports, other runs' `{agentWorkspace}`, undirected workspace search, session chat | Non-authoritative unless promoted |

**Pack supremacy:** For synthesis and gate evidence, the first two planes govern the run. Ambient context may inform Discovery or Factory; it does not substitute for manifest reads or contract-declared datastore paths.

### Closure set (default)

After pre-run refresh and before core execution, the agent's **closure set** is:

1. Workbench standard and distribution pack artifacts reachable from the playbook manifest read chain (see [Read order](#read-order)).
2. Pack `contracts/` referenced by the playbook manifest, its skills, workflows, overlays, or output contracts.
3. `{userDatastore}` subtrees the pack declares readable for this playbook (layout contract, persistence contract, skill `--datastore` paths).
4. `{agentWorkspace}` for **this run only** (including skill scratch under the active run subdirectory).
5. External sources only when a referenced skill procedure authorizes them (for example web research).

### Default deny

Unless [continuity execution](#continuity-modes) applies, do **not** read or treat as synthesis inputs:

- `{userDatastore}/reports/**` except the new report folder being written in the current run (after synthesis, not before).
- `{agentWorkspace}` directories belonging to **other** runs.
- Prior deliverables discovered by undirected search (`Glob`, `Grep`, workspace index) when not named in the closure set.

Prior report folders are **immutable run artifacts**, not a shadow memory system. User-confirmed continuity belongs in contract-declared durable knowledge paths (for example `{userDatastore}/knowledge/`) per pack persistence contracts.

### Authoritative precedence (execution synthesis)

When sources conflict, prefer in order:

1. Playbook manifest and manifest-referenced contracts, skills, workflows, overlays.
2. Resolved playbook inputs and attested defaults (**Inputs Resolved**).
3. Contract-declared datastore paths and skill script outputs from this run.
4. Skill-authorized external fetches from this run.
5. Ambient context (session chat, indexed files) — **non-authoritative** until bound as (2) or included in (3).

### Continuity modes

Default posture is **closure-first** (closure set only; often described as "greenfield" for narrative synthesis). These named modes relax the default **only** when explicitly declared:

| Mode | Trigger | Additional reads allowed |
| --- | --- | --- |
| **Default execution** | Normal playbook run | Closure set only |
| **Continuity execution** | User run request or playbook input names a prior artifact or run id | Named report(s) or registry entries only |
| **Revision execution** | User asks to revise, update, or extend a named prior deliverable | Named target deliverable as edit source |
| **Regression / diff** | Harness, CI, or explicit test request | Prior deliverables for comparison — not for production narrative reuse |

Record the active mode in [pre-run attestation](pre-run-checklist.md#attestation). When mode is not `default`, list every path read outside the default closure set.

### Structural determinism vs narrative independence

Same playbook inputs and datastore state should yield **structurally consistent** outputs (sections, metrics, gate evidence). That is PACS success, not pollution.

**Narrative independence** means prose synthesis comes from closure-set sources and skill-authorized fetches in **this run** — not verbatim reuse of prior report text unless continuity mode explicitly authorizes it.

### Platform enforcement (optional)

Hosts may enforce closure with sandboxes, read-only datastore views, or ignore rules for `{userDatastore}/reports/`. PACS defines **behavior and attestation**; platform mechanics are **platform scope**. See [Workbench guide](../documentation/pacs-workbench-guide.md#execution-closure-platform-patterns) for non-normative patterns.

---

## Execution sequence

Given a pack instance address and resolved playbook:

1. **Refresh** — update workbench standard and distribution pack to latest (unless pinned); complete the [pre-run checklist](pre-run-checklist.md).
2. **Provision** — obtain the distribution repo when no suitable local copy exists (see [Pack provisioning](#pack-provisioning-recommended)).
3. **Read manifests** — `pack.pacs.yaml` → `<playbook-id>.pacs.yaml` → referenced artifacts only.
4. **Bind and declare closure** — set `{userDatastore}`; set or select ephemeral `{agentWorkspace}` (see above); declare execution closure mode and complete closure attestation per [pre-run checklist](pre-run-checklist.md#execution-closure).
5. **Resolve inputs** — run required layer 0 workflows (typically `input-discovery`). Apply manifest `default` values and playbook `defaultResolution` policies when the user did not specify a value (see [`pacs-authoring.md`](pacs-authoring.md#default-resolution-policies)).
6. **Clear gates** — complete workflows and skills; record minimum evidence per gate (see [`pacs-authoring.md`](pacs-authoring.md#gates-and-evidence)).
7. **Run skills** — execute per each `SKILL.md` Procedure; run bundled scripts only when instructed.
8. **Apply overlays** — when manifest `when:` conditions match resolved inputs.
9. **Write outputs** — primary report and contract-required artifacts under `{userDatastore}` per playbook manifest and output contracts.
10. **Self-verify** — complete the [post-run checklist](post-run-checklist.md) against referenced contracts.

### Rules

- Prompt-first; run bundled scripts only when `SKILL.md` instructs.
- No ad-hoc scripts during a run.
- Core output runs without optional overlays unless playbook inputs enable them.
- When contracts and on-disk layout disagree, trust raw files and document the mismatch in the report.
- Do not read `{userDatastore}/reports/` or other runs' `{agentWorkspace}` except under an attested [continuity mode](#continuity-modes).

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

PACS execution guide v0.2. Pairs with PACS authoring standard v0.2.
