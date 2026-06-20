# TeamFoundry Employee Base — APP Pack Sketch

Design reference for the TFY realignment pilot, derived from read-only inspection of `teamfoundry.ai`.

For accepted pilot status, materialized files, simulator preview state, and next actions, see `docs/tfy-stack-realignment/teamfoundry-stack-realignment-plan.md`.

Do not treat manifest blocks or example shape sections in this README as proof that files exist on disk.

## Source Corpus

| TFY artifact | Role |
| --- | --- |
| `foundry/ops/casts/teamfoundry-employee.json` v1.0.5 | Foundation cast; always last in cast stack |
| `foundry/ops/inventories/skills/backup-to-hq-zip/` | Encrypted config backup procedure |
| `foundry/ops/inventories/skills/channel-registry/` | Slack channel/thread routing |
| `foundry/ops/inventories/skills/duckduckgo-search/` | Web search capability |
| `foundry/ops/inventories/skills/message-signing/` | Outbound message signing enforcement |
| `foundry/ops/inventories/habits/daily-backup.json` | Scheduled backup habit |
| `foundry/ops/inventories/hidden-session-wake/universal-agents.md` | Session startup protocol |
| `foundry/ops/inventories/hidden-session-wake/employee-handbook-reference.md` | Handbook load trigger |
| `foundry/ops/inventories/hidden-first-wake/agent-birth.md` | First-run bootstrap ritual |
| `foundry/ops/inventories/hidden-gw-wake/gateway-startup.md` | Gateway startup ritual |
| `foundry/ops/inventories/identity/tfy-employee-identity.md` | Employee identity template |
| `foundry/ops/inventories/memories/` | Memory structure and institutional context |
| `foundry/ops/inventories/bookshelves/employee-handbook/` | Corporate policy |
| `foundry/ops/inventories/hidden-config-json/employee.txt` | Runtime config deltas |
| `hq/ops/forging-requests/SCHEMA-v2.1.md` | Cast composition rules |

## Why This Pilot

TeamFoundry Employee is a strong first pilot because it:

- Is mandatory on every forged assistant (`teamfoundry-employee` MUST be present and last).
- Mixes portable behaviors (routing, signing, backup workflow) with clearly TFY-owned content (identity placeholders, handbook, deployment config).
- Exposes a scheduled-behavior translation question (`daily-backup.json` → APP scheduled playbook → OpenClaw habit).
- Is small enough to complete but rich enough to test APP/TFY boundary decisions from Pillar 3.

## Pack Intent

The pack answers:

> What baseline employee operating behaviors should every TeamFoundry assistant carry, independent of role-specific casts?

It expresses **reusable operating workflows** that role casts (investment-advisor, sysadmin, etc.) assume are already present. It does not define who the employee is, where they deploy, or how Forge/HQ assembles the full assistant.

## Example Shape

```text
teamfoundry-employee-base/
  pack.app.yaml
  playbooks/
    session-readiness/
      playbook.app.yaml
      README.md
    channel-registration/
      playbook.app.yaml
      README.md
    daily-backup/
      playbook.app.yaml
      README.md
  skills/
    backup-to-hq-zip/
      SKILL.md
    channel-registry/
      SKILL.md
    duckduckgo-search/
      SKILL.md
    message-signing/
      SKILL.md
  workflows/
    session-startup.md
    policy-refresh.md
    backup-verification.md
  overlays/
    signed-communication.md
  contracts/
    backup-artifact-contract.md
    routing-registry-contract.md
    message-signature-contract.md
  gates/
    identity-context-loaded.md
    registry-current.md
    backup-passphrase-available.md
```

Skill bodies in this sketch mirror TFY inventory intent. A later pass may replace verbatim copies with `skillRef` entries pointing at curated Agent Skills packages once migration boundaries are validated.

## Playbooks

### `session-readiness`

User/operator intent: begin a work session with correct routing context and memory loaded.

Derived from `universal-agents.md` and the handbook refresh trigger in `employee-handbook-reference.md`.

Requires:

- `workflows/session-startup.md` — registry check, memory load, identity context confirmation
- `workflows/policy-refresh.md` — re-read applicable handbook sections on session restart or high-risk ops

Gates:

- `registry-current` — routing registry readable and schema-valid
- `identity-context-loaded` — assistant identity context resolved by TFY assembly (not defined inside APP)

Uses:

- `channel-registry` skill (registry read path)
- `message-signing` skill (available for subsequent outbound messages)

Outputs:

- Session readiness record (internal run manifest entry; no customer-facing artifact)

### `channel-registration`

User/operator intent: register a Slack channel topic and enable deterministic routing.

Derived from `channel-registry` skill registration flow.

Requires:

- `workflows/session-startup.md` (registry must exist)

Uses:

- `channel-registry` skill

Gates:

- `registry-current`

Outputs:

- Updated routing registry state per `contracts/routing-registry-contract.md`

### `daily-backup`

Operator intent: run the scheduled encrypted backup workflow and report status.

Derived from `daily-backup.json` habit and `backup-to-hq-zip` skill.

Schedule (consumption metadata for TFY translation):

```yaml
schedule:
  at: "04:30"
  timezone: UTC
  days: [monday, tuesday, wednesday, thursday, friday]
  mode: background
```

Requires:

- `workflows/backup-verification.md`

Uses:

- `backup-to-hq-zip` skill
- `message-signing` skill (status notification)

Gates:

- `backup-passphrase-available` — resolved from TFY deployment secrets, not stored in APP

Overlays:

- `signed-communication` — all Slack status messages must carry handbook signature format

Outputs:

- Backup archive artifact per `contracts/backup-artifact-contract.md`
- Signed status notification (success or escalation)

## Pack-Level Cross-Cutting Behavior

### Signed communication overlay

Derived from `message-signing` skill and `EMPLOYEE-HANDBOOK.md` communication standards.

Applied when outbound messages use team communication channels. APP declares the signature contract; TFY supplies agent name, instance, and session identifiers at assembly time.

### Shared skill capabilities

| Skill | APP role |
| --- | --- |
| `backup-to-hq-zip` | Procedure for encrypted backup creation and retention tiers |
| `channel-registry` | Registry schema ownership and routing mutations |
| `duckduckgo-search` | General web search capability available to other playbooks and role casts |
| `message-signing` | Signature validation and auto-append before Slack send |

`duckduckgo-search` is included as pack capability but has no dedicated playbook in this base pack. Role-specific packs may compose it.

## Pack Manifest Sketch

```yaml
appVersion: "0.1"
kind: pack
packId: teamfoundry-employee-base
name: TeamFoundry Employee Base
version: "0.1.0"
description: >
  Baseline operating behaviors shared by all TeamFoundry employees:
  session readiness, channel routing, signed communication, and daily backup.

license: TBD

compatibility:
  agentSkills: ">=1.0"
  runtimes:
    - openclaw
  consumptionProfile:
    intendedConsumer: teamfoundry
    compositionRole: base
    composeOrder: last
    requiresAssemblyContext:
      - identity.name
      - identity.instance
      - deployment.opsChannel
      - deployment.supervisor
      - secrets.backupPassphrase

paths:
  playbooks: playbooks/
  skills: skills/
  workflows: workflows/
  overlays: overlays/
  contracts: contracts/
  gates: gates/

playbooks:
  - id: session-readiness
    path: playbooks/session-readiness/playbook.app.yaml
    activation: session-start
  - id: channel-registration
    path: playbooks/channel-registration/playbook.app.yaml
    activation: on-demand
  - id: daily-backup
    path: playbooks/daily-backup/playbook.app.yaml
    activation: scheduled

packOverlays:
  - id: signed-communication
    kind: policy
    appliesWhen: outbound.channel == "slack"

sourceCorpus:
  repository: teamfoundry.ai
  cast: teamfoundry-employee
  castVersion: "1.0.5"
  readOnly: true
```

## Playbook Manifest Sketches

### `session-readiness`

```yaml
appVersion: "0.1"
kind: playbook
id: session-readiness
packId: teamfoundry-employee-base
version: "0.1.0"
description: Load routing registry, recent memory, and policy context before interaction.

activation: session-start

inputs:
  policyRefreshTrigger:
    type: enum
    values: [session-restart, high-risk-op, periodic]
    default: session-restart

requires:
  - workflow: workflows/session-startup
  - workflow: workflows/policy-refresh

uses:
  - skill: ../../skills/channel-registry
  - skill: ../../skills/message-signing

gates:
  - registry-current
  - identity-context-loaded

outputs:
  primary:
    type: run-record
    pathTemplate: memory/session-readiness/{timestamp}.json
```

### `channel-registration`

```yaml
appVersion: "0.1"
kind: playbook
id: channel-registration
packId: teamfoundry-employee-base
version: "0.1.0"
description: Register a channel topic and enable deterministic Slack routing.

inputs:
  channelTopic:
    type: string
    required: true
  registrationPhrase:
    type: string
    required: false

requires:
  - workflow: workflows/session-startup

uses:
  - skill: ../../skills/channel-registry

gates:
  - registry-current

outputs:
  primary:
    type: registry-update
    contract: contracts/routing-registry-contract.md
```

### `daily-backup`

```yaml
appVersion: "0.1"
kind: playbook
id: daily-backup
packId: teamfoundry-employee-base
version: "0.1.0"
description: Encrypt workspace configuration and report backup status.

schedule:
  at: "04:30"
  timezone: UTC
  days: [monday, tuesday, wednesday, thursday, friday]
  mode: background

inputs:
  agentOpsChannel:
    type: string
    required: true
    resolveFrom: deployment.opsChannel
  supervisorId:
    type: string
    required: true
    resolveFrom: deployment.supervisor

requires:
  - workflow: workflows/backup-verification

uses:
  - skill: ../../skills/backup-to-hq-zip
  - skill: ../../skills/message-signing

gates:
  - backup-passphrase-available

overlays:
  - id: signed-communication
    kind: policy

outputs:
  primary:
    type: archive
    contract: contracts/backup-artifact-contract.md
  notification:
    type: status-message
    contract: contracts/message-signature-contract.md
```

## Contract Sketches

### `routing-registry-contract.md`

- Canonical registry file role: channel/topic/thread routing state
- Mutation authority: `channel-registry` skill
- APP declares schema expectations; TFY/engine adapter chooses runtime path (currently `memory/thread-registry.json` in OpenClaw)

### `backup-artifact-contract.md`

- Encrypted archive naming: `backup-YYYYMMDD_HHMMSS.7z`
- Retention tiers: 7 daily, 4 weekly, 12 monthly
- APP declares artifact shape and retention rules; TFY/HQ owns storage location and git push policy

### `message-signature-contract.md`

- Format: `— Name.Instance.SessionID`
- Applies to all Slack outbound messages except `NO_REPLY`
- APP declares format; TFY assembly supplies name/instance; engine session supplies session id

## What Stays TeamFoundry-Owned

This table is the primary boundary artifact for the pilot.

| Concern | Owner | Examples from TFY corpus | Why not APP |
| --- | --- | --- | --- |
| Employee identity and persona | TFY | `tfy-employee-identity.md` with `FULL_NAME_PLACEHOLDER`, forged `identity` stacks | Identity is per-assistant, customer-specific, and assembled at forge time |
| Corporate policy and governance | TFY | `employee-handbook/`, handbook appendices, violation consequences | Immutable corporate policy; not portable behavior packaging |
| Institutional and customer memory | TFY | `tfy-institutional-memories.md`, `memory-structure.md`, workspace `MEMORY.md` | Context is cultivated per deployment and customer relationship |
| Cast composition rules | TFY | `teamfoundry-employee` MUST be last; Forge FR schema | Assistant construction and precedence are TFY Forge concerns |
| Deployment and HQ lifecycle | TFY | HQ backup paths, snapshot git layout, commissioning, FR/AFR workflows | Operations, not reusable behavior intent |
| Runtime configuration | TFY / engine adapter | `employee.txt`, `employee.auth.json`, model defaults, heartbeat prompt | Engine-native config patches; translation output, not APP source |
| First-run and gateway rituals | TFY / engine adapter | `agent-birth.md`, `gateway-startup.md` | Runtime activation hooks; map to OpenClaw wake/hook artifacts at translation |
| Secrets and auth material | TFY | backup passphrase location, auth profiles, SSH keys in backup scope | Deployment-bound; resolved at assembly, never embedded in APP |
| Slack app provisioning | TFY | `employee-bookshelf/slack-app-manifest.json`, `hidden-slack-app/` | Channel/app installation is deployment operations |
| Agent tooling scripts | TFY / engine adapter | `tfy-config-backup.sh`, `tfy-health-check.sh`, `tfy-backup-verify.sh` | Concrete exec surfaces; adapter may emit but APP references behavior not script paths |
| Supervisor and ops routing targets | TFY | `${AGENT_OPS_CHANNEL}`, `${SUPERVISOR_ID}` in habit prompt | Resolved from deployment profile during assistant assembly |
| Role-specific behavior | TFY role casts / other APP packs | `investment-advisor` skills, Warren habits | Domain behavior belongs in role packs composed before the base pack |
| Translation to deployables | TFY | Ingestion, assembly, OpenClaw habit/cron/hook emission | Accepted TFY-mediated translation model (plan decision 2026-06-20) |

## What APP Owns In This Sketch

| Concern | APP expression |
| --- | --- |
| Session readiness workflow | `session-readiness` playbook + `session-startup` workflow |
| Channel registration behavior | `channel-registration` playbook + `channel-registry` skill |
| Backup operating workflow | `daily-backup` playbook + `backup-to-hq-zip` skill + backup contract |
| Signed outbound communication | `signed-communication` overlay + `message-signing` skill + signature contract |
| Web search capability | `duckduckgo-search` skill reference (capability, not playbook) |
| Scheduled behavior intent | `daily-backup` schedule metadata in playbook manifest |
| Cross-assistant base composition | Pack metadata: `compositionRole: base`, `composeOrder: last` |

## Expected TFY Assembly

When Forge composes an assistant, this pack is one input among many:

```text
assistant instance =
  role cast playbooks/skills        # e.g. investment-advisor (composed first)
  + teamfoundry-employee-base pack  # this sketch (composed last)
  + identity                        # tfy-employee-identity + role identity
  + persona / personality
  + knowledge / bookshelves
  + policies / handbook bindings
  + memories
  + customer context
  + engine profile
  + deployment target
```

APP declares behavior intent. TFY resolves placeholders, binds handbook and identity content, and translates assembled context to engine deployables.

## Illustrative Translation Targets

Design-time mapping from APP elements to OpenClaw preview targets. See `tools/tfy-simulator/` and **Pilot Materialization Status** in the plan for preview artifacts.

| APP element | OpenClaw preview target |
| --- | --- |
| `session-readiness` playbook | Session wake instructions in `hidden-session-wake/` |
| `daily-backup` schedule | `habits/daily-backup.json` cron prompt |
| `channel-registration` playbook | `skills/channel-registry/` activation |
| `signed-communication` overlay | `skills/message-signing/` tool-call enforcement |
| `duckduckgo-search` skill | `skills/duckduckgo-search/` install |
| Pack consumption profile | Forge manifest `source_casts` entry with role `base` |

## Open Questions For Pilot Validation

1. Should `session-readiness` and handbook refresh remain one playbook or split policy refresh into a separate overlay?
2. Should `schedule` live on the playbook manifest, pack manifest, or a dedicated scheduled-behavior kind?
3. Are verbatim skill mirrors acceptable in the first example, or should the pilot use `skillRef` to TFY paths during read-only phase?
4. Does `identity-context-loaded` belong in APP gates if identity content is TFY-owned, or should it be an assembly precondition outside the pack?
5. Is base-pack `composeOrder: last` APP metadata, TFY Forge rule, or both?
