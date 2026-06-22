---
name: backup-to-hq-zip
description: Create an encrypted configuration-state archive with tiered retention for assistant backup workflows.
version: "0.1.0"
sourceCorpus:
  repository: teamfoundry.ai
  path: foundry/ops/inventories/skills/backup-to-hq-zip/SKILL.md
  readOnly: true
---

# backup-to-hq-zip

Create an AES-256 encrypted archive of assistant **configuration state**, apply tiered retention, and produce a timestamped backup artifact suitable for HQ storage.

Used by the `daily-backup` playbook. Storage location, git push policy, and passphrase binding are resolved at TeamFoundry assembly time—not defined in this skill.

## When to Use

- Scheduled or on-demand encrypted backup of assistant configuration state
- Before high-risk configuration changes when a restorable snapshot is prudent
- When a playbook or operator requests a configuration backup with retention rotation

## Procedure

1. **Confirm prerequisites** — encryption tooling available; backup passphrase gate cleared (see playbook gates).
2. **Collect configuration state** — gather included scope (below); exclude content-state patterns (below).
3. **Create archive** — AES-256 encrypted 7z with timestamped name `backup-YYYYMMDD_HHMMSS.7z`.
4. **Apply retention** — rotate prior archives per retention tiers below; keep git-friendly archive sizes.
5. **Return artifact metadata** — filename, size, and success/failure for playbook verification and notification.

Detailed artifact naming and retention rules also appear in `contracts/backup-artifact-contract.md` (not yet materialized in this pilot).

## Retention Policy

| Tier | Count | Criteria |
| --- | --- | --- |
| Daily | 7 | Last 7 days, one per day |
| Weekly | 4 | Sundays (day of week = 0) |
| Monthly | 12 | 1st of each month |

Example timeline (filenames only; storage path is TFY-owned):

```text
backup-20260227_043015.7z   (today — daily)
backup-20260226_043012.7z   (yesterday — daily)
backup-20260223_043010.7z   (Sunday — weekly)
backup-20260201_043000.7z   (1st of month — monthly)
```

## Backup Scope

Describe **what class of state** to include or exclude. The target engine adapter maps these categories to runtime paths and exec surfaces.

### Included — Configuration State

| Category | Intent |
| --- | --- |
| Engine configuration | Core engine settings and credentials needed to restore operation |
| Workspace markdown | Agent workspace markdown files defining behavior and context |
| Installed skills | Skill directories required to restore capabilities |
| Workspace memory | Persistent memory files the assistant relies on across sessions |
| Workspace docs | Operational markdown documentation (excluding large archives) |
| Workspace logs | Recent operational logs useful for diagnosis after restore |
| Version-control identity | SSH keys and git identity needed to authenticate after restore |
| Package hub state | Local package hub metadata if present |

### Excluded — Content State

| Pattern class | Reason |
| --- | --- |
| Session transcripts | Large; preserved in communication channels |
| Renderable media | Screenshots and canvas content can be regenerated |
| Downloaded media | Re-fetchable from source |
| LLM completion cache | Regenerable |
| Conversation and document archives | Historical transcripts; large |
| Generated reports (PDF, HTML) | Belong in durable file storage, not config backup |
| Dependency trees | Reinstallable (e.g. node_modules) |

## Archive Contents

Each archive should include a `MANIFEST.txt` listing:

- Included categories and representative sources
- Excluded pattern classes and rationale
- Retention policy summary
- High-level restoration guidance (adapter-specific steps are TFY/engine-owned)

## Security

- Use AES-256 encryption for archives.
- Never embed the passphrase inside the archive.
- Passphrase availability is a deployment gate (`backup-passphrase-available`); binding location is TFY-owned.
- SSH keys may be included because they are required to restore authenticated operation; treat archives as sensitive.

## Outputs

| Output | Description |
| --- | --- |
| Primary archive | Encrypted `backup-YYYYMMDD_HHMMSS.7z` per backup artifact contract |
| Manifest | In-archive `MANIFEST.txt` documenting scope and policy |

## Boundaries

| Concern | Owner |
| --- | --- |
| What to back up and retention rules | APP (this skill + backup artifact contract) |
| HQ snapshot storage path and git push | TeamFoundry operations |
| Passphrase file location and secret binding | TeamFoundry assembly |
| Concrete exec scripts and engine paths | Engine adapter (translation output) |
| Restoration runbook on fresh infrastructure | TeamFoundry / engine adapter |
