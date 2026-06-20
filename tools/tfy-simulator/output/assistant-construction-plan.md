# Assistant Construction Plan (Preview)

**Run:** `daily-backup-openclaw-preview-001`  
**Pack:** `teamfoundry-employee-base` v0.1.0  
**Playbook:** `daily-backup`  
**Engine profile:** `openclaw`  
**Status:** Hand-authored preview (simulator not implemented)

## Assembly Inputs

| Input layer | Source | Preview value |
| --- | --- | --- |
| Role cast | (none for this preview) | — |
| APP pack | `examples/teamfoundry-employee-base/pack.app.yaml` | `compositionRole: base`, `composeOrder: last` |
| Identity | TFY assembly | Warren.001 |
| Deployment | TFY assembly | ops channel `agent-ops`, supervisor `supervisor-id` |
| Secrets | TFY assembly | `backupPassphrase` resolved (not stored in APP) |
| Engine profile | Simulator input | openclaw |

## Pack Ingest Summary

- **Pack id:** `teamfoundry-employee-base`
- **Materialized playbooks:** `daily-backup` only
- **Consumption profile:** `intendedConsumer: teamfoundry`, base pack, compose last
- **Required assembly context:** identity.name, identity.instance, deployment.opsChannel, deployment.supervisor, secrets.backupPassphrase

## Playbook Assembly — daily-backup

### Resolved inputs

| Input | resolveFrom | Resolved value |
| --- | --- | --- |
| `agentOpsChannel` | `deployment.opsChannel` | `agent-ops` |
| `supervisorId` | `deployment.supervisor` | `supervisor-id` |

### Gates

| Gate | Resolution |
| --- | --- |
| `backup-passphrase-available` | TFY checks deployment secret binding; mock preview assumes available |

### Skill dependencies

| APP reference | Resolution strategy | Preview action |
| --- | --- | --- |
| `../../skills/backup-to-hq-zip` | **Missing on disk** — not materialized | Map to TFY corpus skill `foundry/ops/inventories/skills/backup-to-hq-zip/` via adapter inventory install |
| `../../skills/message-signing` | **Missing on disk** — not materialized | Map to TFY corpus skill `foundry/ops/inventories/skills/message-signing/` via adapter inventory install |

### Workflow dependencies

| APP reference | Status | Preview action |
| --- | --- | --- |
| `workflows/backup-verification` | **Missing on disk** | Emit warning; translation falls back to habit prompt steps from TFY corpus habit |

### Overlays

| Overlay | Applies when | Assembly binding |
| --- | --- | --- |
| `signed-communication` (policy) | Outbound Slack status messages | Identity Warren.001 + session id at runtime |

### Outputs

| Output | Contract | Owner at runtime |
| --- | --- | --- |
| Primary archive | `contracts/backup-artifact-contract.md` (**missing**) | TFY/HQ snapshot path under `teamHQ/Agents-InService/Warren.001/snapshots/` |
| Status notification | `contracts/message-signature-contract.md` (**missing**) | Slack via engine message tool |

## Translation Plan (OpenClaw)

1. Emit `habits/daily-backup.json` from playbook `schedule` + assembled inputs + skill-backed prompt steps.
2. Reference-install `backup-to-hq-zip` and `message-signing` skills from TFY corpus paths (not APP-local copies).
3. Apply `signed-communication` overlay to notification step in habit prompt.
4. Do **not** emit identity, handbook, or HQ git-push policy from APP — those remain TFY assembly/operations inputs.

## Composition Note

When Forge composes a full assistant, this base pack is applied **last** after role casts. This preview exercises only the base pack playbook in isolation.
