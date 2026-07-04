# Standard

Normative PACS standard files.

| File | Purpose |
| --- | --- |
| [`pacs-authoring.md`](pacs-authoring.md) | Authoring standard — layout, layers, execution outcomes |
| [`pacs-execution.md`](pacs-execution.md) | Execution guide — refresh, bind, run, verify (operational) |
| [`pre-run-checklist.md`](pre-run-checklist.md) | Contract checklist for pre-run refresh (workbench and pack) |
| [`post-run-checklist.md`](post-run-checklist.md) | Contract checklist for post-run self-verification |
| [`pack.manifest.schema.json`](pack.manifest.schema.json) | JSON Schema for `pack.pacs.yaml` |
| [`playbook.manifest.schema.json`](playbook.manifest.schema.json) | JSON Schema for `<playbook-id>.pacs.yaml` |
| [`validate-manifests.py`](validate-manifests.py) | Validate manifests and reference-instance layout (author/CI only) |
| [`requirements.txt`](requirements.txt) | Python dependencies for `validate-manifests.py` |

Manifests are **YAML on disk**; schemas are **JSON** for validation tooling.

Reference instances (format study only): [`../documentation/examples/`](../documentation/examples/). Product guide: [`../documentation/pacs-workbench-guide.md`](../documentation/pacs-workbench-guide.md).
