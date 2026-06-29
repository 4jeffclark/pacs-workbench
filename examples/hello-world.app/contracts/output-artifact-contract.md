# Hello World Output Artifacts

## Report folder pattern

```text
{userDatastore}/reports/<GenerationTimestamp>-HelloWorld/
```

| Token | Format |
| --- | --- |
| `GenerationTimestamp` | `YYYYMMDD-HHMMSS` (wall-clock at folder creation) |
| `HelloWorld` | Fixed playbook report id |

Example:

```text
{userDatastore}/reports/20260623-143052-HelloWorld/
```

## Required artifacts

| File | Role |
| --- | --- |
| `Report.md` | Self-contained human-readable run output |

## Report.md

Minimum sections:

1. **Greeting** — core output from `compose-greeting` skill
2. **Welcome banner** — present only when `banner: true` (overlay)
3. **Sign-off** — present only when `friendly: true` (overlay)
4. **Appendix: Inputs Resolved** — final resolved playbook inputs

Report assembly (section order, timestamp folder, Inputs Resolved table) is **agent responsibility** per the output contract. The core skill produces greeting text only.

### Appendix: Inputs Resolved (template)

```markdown
## Appendix: Inputs Resolved

| Input | Value | Status |
| --- | --- | --- |
| recipient | Alice | confirmed |
| friendly | false | default |
| banner | false | default |
```

## Timestamp rules

- Use actual generation time — no placeholders
- Never overwrite an existing folder; create a new timestamp if the path exists

## Post-run verification

Self-verify per [APP post-run checklist](https://github.com/4jeffclark/agent-playbook-pack/blob/main/standard/post-run-checklist.md) after writing the report folder.
