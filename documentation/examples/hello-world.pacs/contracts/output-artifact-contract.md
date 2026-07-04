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

Canonical section order (omit overlay sections when their `when:` condition is false):

1. **Welcome banner** — presentation overlay when `banner: true`
2. **Greeting** — core output from `compose-greeting` skill
3. **Sign-off** — enrichment overlay when `friendly: true`
4. **Appendix: Inputs Resolved** — final resolved playbook inputs

Presentation overlays precede core output; enrichment overlays follow core output. Report assembly (timestamp folder, Inputs Resolved table) is **agent responsibility** per this contract. The core skill produces greeting text only.

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

Self-verify per [PACS post-run checklist](https://github.com/4jeffclark/agent-playbook-pack/blob/main/standard/post-run-checklist.md) after writing the report folder.
