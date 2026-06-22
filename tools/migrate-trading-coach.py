#!/usr/bin/env python3
"""One-shot migration: legacy TradingCoach (ASP) -> APP trading-coach.app instance.

Reads C:\\code\\trading-coach (read-only). Writes examples/ as APP distribution repo root.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

LEGACY = Path(r"C:\code\trading-coach")
REPO_ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = REPO_ROOT
DIST_ROOT = REPO_ROOT / "examples"
PACK_ROOT = DIST_ROOT / "trading-coach.app"
PACK_ID = "trading-coach"
APP_FRAMEWORK_REPO = "https://github.com/4jeffclark/agent-playbook-pack.git"

PLAYBOOKS = [
    "aggregate-state-review",
    "environment-review",
    "unit-decision-review",
    "activity-period-review",
    "source-profile",
]

CAPABILITIES = sorted(
    p.stem
    for p in (LEGACY / "capabilities").glob("*.md")
    if p.name != "README.md"
)

WORKFLOWS = [
    "datastore-merge-and-validate",
    "structured-input-discovery",
    "period-scope-confirmation",
]

GATE_IDS = [
    "datastore-merge-complete",
    "inputs-resolved",
    "period-confirmed",
    "holdings-map-confirmed",
    "theme-map-confirmed",
    "thesis-registry-confirmed",
    "entry-interview",
    "entry-interview-complete",
]


def rewrite_text(text: str) -> str:
    """Adapt legacy repo-relative paths to APP userDatastore and layer folders."""
    text = text.replace("DATASTORE_CONTRACT.md", "contracts/datastore-contract.md")
    text = text.replace("docs/holdings-taxonomy.md", "contracts/holdings-taxonomy.md")
    text = text.replace(
        "docs/persistent-knowledge-model.md", "contracts/persistent-knowledge-model.md"
    )
    text = text.replace("data/README.md", "contracts/user-datastore-layout.md")
    text = text.replace("reports/README.md", "contracts/report-artifact-contract.md")
    text = re.sub(r"(?<![\w/])capabilities/", "layer1-skills/", text)
    text = re.sub(r"(?<![\w/])workflows/", "layer0-workflows/", text)
    text = re.sub(r"(?<![\w/])playbooks/", "layer3-playbooks/", text)
    # Datastore paths (legacy in-repo -> userDatastore)
    text = re.sub(r"(?<!\{)(?<![\w/])data/raw/", "{userDatastore}/data/raw/", text)
    text = re.sub(r"(?<!\{)(?<![\w/])data/canonical/", "{userDatastore}/data/canonical/", text)
    text = re.sub(r"(?<!\{)(?<![\w/])data/knowledge/", "{userDatastore}/data/knowledge/", text)
    text = re.sub(r"(?<!\{)(?<![\w/])reports/", "{userDatastore}/reports/", text)
    text = re.sub(r"(?<!\{)(?<![\w/])inputs/", "{userDatastore}/inputs/", text)
    return text


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def skill_id_from_ref(ref: str) -> str:
    ref = ref.replace("capabilities/", "").replace("layer1-skills/", "")
    return ref.strip("/")


def convert_skill(cap_id: str) -> None:
    md_src = LEGACY / "capabilities" / f"{cap_id}.md"
    asp_src = LEGACY / "capabilities" / f"{cap_id}.asp.yaml"
    dest_dir = PACK_ROOT / "layer1-skills" / cap_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    asp = load_yaml(asp_src) if asp_src.exists() else {}
    body = rewrite_text(md_src.read_text(encoding="utf-8"))

    # Strip ASP capability header; keep procedure content from first ## Purpose or full body
    if body.startswith("# Capability"):
        parts = re.split(r"\n## (?:Capability Id|Purpose|Procedure)\n", body, maxsplit=3)
        if len(parts) >= 3:
            body = parts[-1].strip()
        else:
            body = re.sub(r"^# Capability[^\n]*\n+", "", body, count=1).strip()

    name = cap_id
    description = asp.get("description") or f"TradingCoach skill: {cap_id}"
    kind = asp.get("capabilityKind", "")
    header = (
        f"---\nname: {name}\ndescription: {description}\n"
        f"sourceCorpus:\n  repository: trading-coach\n"
        f"  path: capabilities/{cap_id}/\n  readOnly: true\n"
    )
    if kind:
        header += f"metadata:\n  legacyCapabilityKind: {kind}\n"
    header += "---\n\n"
    (dest_dir / "SKILL.md").write_text(header + body, encoding="utf-8")


def convert_workflow(wf_id: str) -> None:
    src = LEGACY / "workflows" / f"{wf_id}.md"
    dest = PACK_ROOT / "layer0-workflows" / f"{wf_id}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(rewrite_text(src.read_text(encoding="utf-8")), encoding="utf-8")


def convert_overlay(playbook_id: str, overlay_file: Path) -> None:
    rel = overlay_file.relative_to(LEGACY / "playbooks" / playbook_id / "overlays")
    if rel.suffix != ".md":
        return
    dest = PACK_ROOT / "layer3-playbooks" / playbook_id / "overlays" / rel.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(rewrite_text(overlay_file.read_text(encoding="utf-8")), encoding="utf-8")


def convert_ref_item(item) -> dict | str:
    if isinstance(item, str):
        if item.startswith("workflows/"):
            return {"workflow": f"../../layer0-workflows/{item.split('/', 1)[1]}"}
        return item
    if not isinstance(item, dict):
        return item
    out = dict(item)
    if "id" in out:
        sid = skill_id_from_ref(out["id"])
        out.pop("id", None)
        out.pop("capabilityKind", None)
        out["skill"] = f"../../layer1-skills/{sid}"
    if "playbook" in out:
        out["playbook"] = out["playbook"]
    return out


def convert_playbook(playbook_id: str) -> None:
    asp_path = LEGACY / "playbooks" / playbook_id / f"{playbook_id}.asp.yaml"
    playbook_md = LEGACY / "playbooks" / playbook_id / "playbook.md"
    dest_dir = PACK_ROOT / "layer3-playbooks" / playbook_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    asp = load_yaml(asp_path)
    app: dict = {
        "appVersion": "0.1",
        "kind": "playbook",
        "id": asp.get("id", playbook_id),
        "packId": PACK_ID,
        "version": str(asp.get("version", "1.0.0")),
        "description": asp.get("description", ""),
    }
    if asp.get("playbookReportId"):
        app["playbookReportId"] = asp["playbookReportId"]

    inputs = asp.get("inputs") or {}
    clean_inputs = {}
    for key, val in inputs.items():
        if isinstance(val, dict):
            val = {k: v for k, v in val.items() if k != "aspNote"}
        clean_inputs[key] = val
    if clean_inputs:
        app["inputs"] = clean_inputs

    requires = []
    for item in asp.get("requires") or []:
        if isinstance(item, str) and item.startswith("workflows/"):
            requires.append({"workflow": f"../../layer0-workflows/{item.split('/', 1)[1]}"})
        else:
            requires.append(item)
    if requires:
        app["requires"] = requires

    for verb in ("uses", "embeds"):
        items = asp.get(verb) or []
        converted = [convert_ref_item(i) for i in items]
        if converted:
            app[verb] = converted

    references = asp.get("references") or []
    if references:
        app["references"] = references

    overlays = []
    for item in asp.get("overlays") or []:
        if isinstance(item, dict):
            oid = item.get("id", "")
            oid = oid.replace("overlays/", "")
            entry = {
                "id": oid,
                "path": f"overlays/{oid}.md",
                "kind": item.get("overlayKind", "evaluation"),
            }
            if "when" in item:
                entry["when"] = item["when"]
            overlays.append(entry)
    if overlays:
        app["overlays"] = overlays

    gates = asp.get("gates")
    if gates:
        app["gates"] = gates

    report_id = asp.get("playbookReportId", playbook_id)
    app["outputs"] = {
        "primary": {
            "type": "report",
            "pathTemplate": (
                f"{{userDatastore}}/reports/{{timestamp}}-{report_id}-"
                "{{analysisPeriodStart}}-{{analysisPeriodEnd}}/Report.md"
            ),
            "contract": "contracts/report-artifact-contract.md",
        },
        "runManifest": {
            "type": "run-record",
            "pathTemplate": (
                f"{{userDatastore}}/reports/{{timestamp}}-{report_id}-"
                "{{analysisPeriodStart}}-{{analysisPeriodEnd}}/run-manifest.yaml"
            ),
        },
    }
    artifacts = asp.get("outputs", {}).get("artifacts") if isinstance(asp.get("outputs"), dict) else None
    if artifacts:
        app["outputs"]["artifacts"] = artifacts

    (dest_dir / "playbook.app.yaml").write_text(dump_yaml(app), encoding="utf-8")
    if playbook_md.exists():
        (dest_dir / "README.md").write_text(
            rewrite_text(playbook_md.read_text(encoding="utf-8")), encoding="utf-8"
        )

    overlay_dir = LEGACY / "playbooks" / playbook_id / "overlays"
    if overlay_dir.exists():
        for f in overlay_dir.glob("*.md"):
            convert_overlay(playbook_id, f)


def write_gates() -> None:
    gate_dir = PACK_ROOT / "gates"
    gate_dir.mkdir(parents=True, exist_ok=True)
    descriptions = {
        "datastore-merge-complete": "Datastore merge and validation workflow completed successfully.",
        "inputs-resolved": "Structured input discovery completed; required inputs resolved.",
        "period-confirmed": "Analysis period boundaries confirmed.",
        "holdings-map-confirmed": "Holdings standards map confirmed for the selected rollup lens.",
        "theme-map-confirmed": "Theme map confirmed when rollupLens is theme or thesis.",
        "thesis-registry-confirmed": "Thesis registry confirmed when rollupLens is thesis.",
        "entry-interview": "Evaluation entry interview completed when evaluation overlay is active.",
        "entry-interview-complete": "Evaluation entry interview capability gate cleared.",
    }
    for gid in GATE_IDS:
        text = f"# Gate — {gid}\n\n{descriptions.get(gid, 'Behavior-contract precondition.')}\n"
        (gate_dir / f"{gid}.md").write_text(text, encoding="utf-8")


def write_contracts() -> None:
    contract_dir = PACK_ROOT / "contracts"
    contract_dir.mkdir(parents=True, exist_ok=True)

    mappings = [
        (LEGACY / "DATASTORE_CONTRACT.md", "datastore-contract.md"),
        (LEGACY / "docs" / "holdings-taxonomy.md", "holdings-taxonomy.md"),
        (LEGACY / "docs" / "persistent-knowledge-model.md", "persistent-knowledge-model.md"),
        (LEGACY / "data" / "README.md", "user-datastore-layout.md"),
        (LEGACY / "reports" / "README.md", "report-artifact-contract.md"),
        (LEGACY / "docs" / "agent-bootstrap.md", "execution-bootstrap.md"),
        (LEGACY / "docs" / "agent-layer-integration.md", "agent-layer-integration.md"),
    ]
    for src, name in mappings:
        if src.exists():
            text = rewrite_text(src.read_text(encoding="utf-8"))
            (contract_dir / name).write_text(text, encoding="utf-8")

    layout_header = (
        "# TradingCoach User Datastore Layout\n\n"
        "This pack owns its datastore layout. Bind `userDatastore` to a host directory; "
        "use this structure beneath it (legacy TradingCoach `data/` and `reports/` layout).\n\n"
        "```text\n"
        "{userDatastore}/\n"
        "  data/\n"
        "    raw/etrade/\n"
        "    canonical/\n"
        "    knowledge/\n"
        "  reports/\n"
        "  inputs/\n"
        "```\n\n"
    )
    layout_path = contract_dir / "user-datastore-layout.md"
    if layout_path.exists():
        layout_path.write_text(
            layout_header + layout_path.read_text(encoding="utf-8"), encoding="utf-8"
        )


def write_pack_manifest() -> None:
    legacy_readme = (LEGACY / "README.md").read_text(encoding="utf-8")
    pack = {
        "appVersion": "0.1",
        "kind": "pack",
        "packId": PACK_ID,
        "name": "TradingCoach",
        "version": "3.1.0",
        "description": "Structured trading performance reviews and portfolio analysis playbooks.",
        "license": "TBD",
        "compatibility": {"agentSkills": ">=1.0"},
        "inputs": {
            "userDatastore": {
                "type": "datastore",
                "required": True,
                "description": "User-controlled storage per contracts/user-datastore-layout.md",
                "layoutContract": "contracts/user-datastore-layout.md",
            },
            "agentWorkspace": {
                "type": "workspace",
                "required": True,
                "description": "Agent-controlled temp and intermediate execution artifacts",
            },
        },
        "playbooks": list(PLAYBOOKS),
        "sourceCorpus": {
            "repository": "trading-coach",
            "readOnly": True,
            "migratedFrom": "AgenticSkillPack v3.1",
        },
    }
    (PACK_ROOT / "pack.app.yaml").write_text(dump_yaml(pack), encoding="utf-8")

    intro = (
        "# TradingCoach\n\n"
        f"`{PACK_ID}.app/` is an [AgentPlaybookPack]({APP_FRAMEWORK_REPO}) (APP) instance "
        f"as defined at [github.com/4jeffclark/agent-playbook-pack]({APP_FRAMEWORK_REPO}).\n\n"
        "Migrated from legacy TradingCoach (ASP v3.1). "
        "Persistent data and reports belong under the bound `userDatastore` "
        "(see `contracts/user-datastore-layout.md`), not in this behavior repo.\n\n"
        "## Playbooks\n\n"
        "| Playbook id | Report id | Path |\n"
        "| --- | --- | --- |\n"
    )
    for pid in PLAYBOOKS:
        asp = load_yaml(LEGACY / "playbooks" / pid / f"{pid}.asp.yaml")
        rid = asp.get("playbookReportId", pid)
        intro += f"| `{pid}` | `{rid}` | [layer3-playbooks/{pid}/](layer3-playbooks/{pid}/) |\n"
    intro += (
        "\n## Execution\n\n"
        "Invoke via APP execution interface: repo address, directive (`pack: trading-coach`, "
        "`playbook: <id>`), and optional partial `inputs`. See `APP-EXECUTION.md`.\n\n"
        "---\n\n"
        "## Legacy Product README (reference)\n\n"
    )
    (PACK_ROOT / "README.md").write_text(
        intro + rewrite_text(legacy_readme), encoding="utf-8"
    )


def write_app_execution() -> None:
    """Copy framework guide and append TradingCoach instance notes."""
    framework = (WORKBENCH / "docs" / "app-execution.md").read_text(encoding="utf-8")
    appendix = (
        "\n---\n\n"
        "## TradingCoach execution notes\n\n"
        "- **Prompt-first** — follow skill and workflow procedures\n"
        "- **Report folders** — `{userDatastore}/reports/<timestamp>-<PlaybookReportId>-"
        "<AnalysisStart>-<AnalysisEnd>/` per `contracts/report-artifact-contract.md`\n"
        "- **Run record** — canonical `run-manifest.yaml`; `Manifest.md` optional\n"
        "- **Core vs augmented** — `evaluation: false` runs core output only\n\n"
        "### Required contracts\n\n"
        "| Contract | Use |\n"
        "| --- | --- |\n"
        "| `contracts/user-datastore-layout.md` | Bind `userDatastore` structure |\n"
        "| `contracts/datastore-contract.md` | Merge and validation |\n"
        "| `contracts/holdings-taxonomy.md` | Rollup lens gates |\n"
        "| `contracts/report-artifact-contract.md` | Report naming and contents |\n"
        "| `contracts/persistent-knowledge-model.md` | Knowledge promotion |\n\n"
        "### Superseded\n\n"
        "`contracts/execution-bootstrap.md` — legacy ASP bootstrap; use `APP-EXECUTION.md`.\n"
    )
    header = (
        "# APP Execution Guide\n\n"
        "Instance copy for **TradingCoach** (`trading-coach.app/`). "
        "Framework source: `docs/app-execution.md` in the AgentPlaybookPack workbench.\n\n"
        "---\n\n"
    )
    body = framework.split("---\n\n", 1)[-1] if framework.startswith("# APP") else framework
    (PACK_ROOT / "APP-EXECUTION.md").write_text(header + body + appendix, encoding="utf-8")


def write_distribution_readme() -> None:
    text = (
        "# TradingCoach APP Distribution Repo\n\n"
        "APP distribution repo root (workbench path: `examples/`). "
        "Contains indexed APP instances only.\n\n"
        "## Packs\n\n"
        "| Pack | Path | Description |\n"
        "| --- | --- | --- |\n"
        "| TradingCoach | [trading-coach.app/](trading-coach.app/) | "
        "Portfolio analysis and trading performance review playbooks |\n\n"
        "## Execution\n\n"
        "```yaml\n"
        "appRepo: <path-to-this-repo>\n"
        "directive:\n"
        "  pack: trading-coach\n"
        "  playbook: aggregate-state-review\n"
        "inputs:\n"
        "  userDatastore: ~/TradingCoachData\n"
        "```\n"
    )
    (DIST_ROOT / "README.md").write_text(text, encoding="utf-8")


def ensure_layer2_readme() -> None:
    d = PACK_ROOT / "layer2-overlays"
    d.mkdir(parents=True, exist_ok=True)
    (d / "README.md").write_text(
        "# Pack-level overlays\n\n"
        "TradingCoach overlays are playbook-scoped under `layer3-playbooks/<id>/overlays/`.\n",
        encoding="utf-8",
    )


def clean_dest() -> None:
    if PACK_ROOT.exists():
        shutil.rmtree(PACK_ROOT)
    PACK_ROOT.mkdir(parents=True)


def main() -> None:
    if not LEGACY.exists():
        raise SystemExit(f"Legacy repo not found: {LEGACY}")

    clean_dest()
    for cap in CAPABILITIES:
        convert_skill(cap)
    for wf in WORKFLOWS:
        convert_workflow(wf)
    for pb in PLAYBOOKS:
        convert_playbook(pb)
    write_gates()
    write_contracts()
    write_pack_manifest()
    write_app_execution()
    ensure_layer2_readme()
    write_distribution_readme()
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "baseline-app-skills.py")],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "materialize-skill-scripts.py")],
        check=True,
    )
    print(f"Migrated to {PACK_ROOT}")
    print(f"  skills: {len(CAPABILITIES)}")
    print(f"  workflows: {len(WORKFLOWS)}")
    print(f"  playbooks: {len(PLAYBOOKS)}")


if __name__ == "__main__":
    main()
