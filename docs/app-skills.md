# APP Skills Baseline

APP **layer1-skills** are [agentskills.io](https://agentskills.io/specification) Agent Skills. APP does not define an alternate skill format, execution mode, or scripting tier.

Playbooks reference skills by directory path. Skill behavior lives entirely in the skill directory.

---

## Skill directory (required shape)

Every APP skill is a directory with **`SKILL.md` required** and these **optional** subdirectories per the Agent Skills specification:

```text
layer1-skills/<skill-id>/
  SKILL.md          # required — frontmatter + instructions
  scripts/          # optional — executable code the agent may run
  references/       # optional — documentation loaded on demand
  assets/           # optional — templates, schemas, static resources
```

Reference: [Agent Skills specification](https://agentskills.io/specification), [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts).

### Baseline rule

**Every materialized skill directory includes `scripts/run.py`** (and `scripts/README.md`) when the pack ships bundled executables. TradingCoach uses a shared stdlib library at `assets/tc-lib/` imported by each skill's `scripts/run.py`.

Empty `scripts/` with only README is not the TradingCoach reference pattern once scripts are materialized — each skill's `SKILL.md` **Scripts** section documents `run.py`.

---

## `SKILL.md` frontmatter

Required fields (agentskills.io):

| Field | Rule |
| --- | --- |
| `name` | kebab-case; must match directory name |
| `description` | what the skill does and when to use it (≤ 1024 chars) |

Optional fields (use when applicable):

| Field | Rule |
| --- | --- |
| `license` | skill license |
| `compatibility` | environment requirements when scripts or tools need them (e.g. `Requires Python 3.11+`) |
| `metadata` | string key-value pairs only (legacy ids, migration source, pack-specific tags) |

APP-specific migration fields belong in `metadata`, not custom top-level frontmatter keys.

Example:

```yaml
---
name: period-weight-reconstruction
description: Reconstruct period boundary holdings weights from canonical datastore tables. Use when building aggregate state or weight tables for a confirmed analysis period.
compatibility: Requires Python 3.11+ when running bundled scripts
metadata:
  legacyCapabilityKind: analyze
  sourceRepository: trading-coach
  sourcePath: capabilities/period-weight-reconstruction/
---
```

---

## `SKILL.md` body sections

Recommended section order:

1. **Procedure** — step-by-step instructions (required content)
2. **Scripts** — list bundled scripts and how to run them (required section; state "none" if empty)
3. **References** — pointers to `references/` or pack `contracts/`
4. **Outputs** — artifacts produced
5. **Used by** — playbooks or overlays that invoke this skill (pack documentation; not part of agentskills.io)

### Scripts section (required in APP skills)

Every `SKILL.md` includes a **Scripts** section. When scripts exist, list them with relative paths from the skill directory:

```markdown
## Scripts

Run from this skill directory. Paths are relative to the skill root per agentskills.io.

| Script | Purpose |
| --- | --- |
| `scripts/reconstruct.py` | Rebuild boundary weights from canonical holdings and activity tables |

```bash
python3 scripts/reconstruct.py --datastore "$USER_DATASTORE" --start YYYYMMDD --end YYYYMMDD
```
```

When no scripts are bundled yet:

```markdown
## Scripts

No bundled scripts. Follow the procedure above. Scripts may be added under `scripts/` per `docs/app-skills.md`.
```

---

## `scripts/` directory

- Contains **pack-authored, versioned** executable code the agent may run when `SKILL.md` instructs it to.
- Scripts must be **self-contained** or declare dependencies inline (see [agentskills.io using scripts](https://agentskills.io/skill-creation/using-scripts)).
- Use **relative paths** in `SKILL.md` (e.g. `scripts/validate.py`, not absolute paths).
- Write machine-readable output to stdout; status messages to stderr.
- Scripts read/write **`{userDatastore}`** and **`{agentWorkspace}`** paths bound at execution — not the APP behavior repo.

`scripts/README.md` in each skill documents bundled scripts or states that none exist yet.

### What scripts are not

- **Not ad-hoc code invented during a playbook run** — runtimes must not treat workspace improvisation as the skill contract.
- **Not a replacement for `SKILL.md`** — instructions remain authoritative for intent, inputs, outputs, and edge cases.
- **Not APP manifest fields** — scripting is entirely inside the agentskills.io skill directory.

---

## `references/` and `assets/`

- **`references/`** — long procedures, column specs, checklists, contract excerpts loaded on demand (progressive disclosure).
- **`assets/`** — templates, sample files, schemas copied or filled during execution.

Prefer `references/` over bloated `SKILL.md` bodies (> ~500 lines or > ~5000 tokens recommended max).

---

## Progressive disclosure

Per agentskills.io:

1. **Metadata** — `name` and `description` at catalog time
2. **Instructions** — full `SKILL.md` when the skill activates
3. **Resources** — `scripts/`, `references/`, `assets/` only when needed

APP playbooks should activate only skills required for the resolved playbook and lenses.

---

## Runtime and compatibility

Supported script languages **depend on the agent implementation** (agentskills.io). Common: Python, Bash, JavaScript.

When a skill bundles scripts:

1. Set `compatibility` in `SKILL.md` frontmatter when requirements are non-obvious.
2. Pack Store listings may aggregate skill `compatibility` for discovery.
3. Runtimes that cannot execute bundled scripts cannot claim full fidelity for that skill unless the skill author documents an equivalent manual procedure in `SKILL.md`.

APP does not define a separate "script-assisted" mode — only whether the skill directory includes `scripts/` and whether `SKILL.md` instructs the agent to run them.

---

## Validation

Validate skills with the agentskills.io reference tooling when available:

```bash
skills-ref validate ./layer1-skills/<skill-id>
```

Pack authors should keep `name` aligned with the directory name and descriptions keyword-rich for agent discovery.

---

## Related docs

| Doc | Role |
| --- | --- |
| [`agent-skills-integration.md`](agent-skills-integration.md) | How APP composes skills in playbooks |
| [`app-execution.md`](app-execution.md) | How execution agents activate skills |
| [`../schema/app-manifest-v0.1.md`](../schema/app-manifest-v0.1.md) | Playbook `uses:` skill references |
