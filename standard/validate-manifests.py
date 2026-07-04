#!/usr/bin/env python3
"""Validate PACS YAML manifests and reference-instance layout conventions."""

from __future__ import annotations

import json
import sys
from pathlib import Path

STANDARD_DIR = Path(__file__).resolve().parent
REPO_ROOT = STANDARD_DIR.parent
EXAMPLES_DIR = REPO_ROOT / "documentation" / "examples"

PACK_SCHEMA = STANDARD_DIR / "pack.manifest.schema.json"
PLAYBOOK_SCHEMA = STANDARD_DIR / "playbook.manifest.schema.json"


def _load_deps():
    try:
        import yaml  # type: ignore
        from jsonschema import Draft202012Validator  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "Missing dependencies. Install with: pip install pyyaml jsonschema"
        ) from exc
    return yaml, Draft202012Validator


def _load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_pack_manifest(path: Path) -> bool:
    return path.name == "pack.pacs.yaml"


def _is_playbook_manifest(path: Path) -> bool:
    return path.name.endswith(".pacs.yaml") and path.name != "pack.pacs.yaml"


def _pack_root(path: Path) -> Path | None:
    for parent in path.parents:
        if parent.name.endswith(".pacs"):
            return parent
    return None


def _playbook_id_from_manifest(path: Path) -> str:
    if path.name.endswith(".pacs.yaml") and path.name != "pack.pacs.yaml":
        return path.name[: -len(".pacs.yaml")]
    return path.stem


def _discover_manifests(root: Path) -> tuple[list[Path], list[Path]]:
    packs = sorted(root.glob("**/*.pacs/pack.pacs.yaml"))
    playbooks: list[Path] = []
    for pack_manifest in packs:
        pack_root = pack_manifest.parent
        for path in sorted(pack_root.glob("layer3-playbooks/*/*.pacs.yaml")):
            if path.name == "playbook.pacs.yaml":
                continue
            if _playbook_id_from_manifest(path) == path.parent.name:
                playbooks.append(path)
    return packs, playbooks


def _validate_file(path: Path, validator, label: str) -> list[str]:
    yaml = _load_deps()[0]
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: YAML parse error: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: manifest root must be a mapping"]

    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"{path}: [{label}] {loc}: {error.message}")
    return errors


def _validate_playbook_path(path: Path) -> list[str]:
    errors: list[str] = []
    if path.name == "playbook.pacs.yaml":
        errors.append(f"{path}: legacy playbook.pacs.yaml; use <playbook-id>.pacs.yaml")
    if _playbook_id_from_manifest(path) != path.parent.name:
        errors.append(
            f"{path}: playbook manifest filename must match folder "
            f"(expected {path.parent.name}.pacs.yaml)"
        )
    return errors


def _validate_playbook_id(path: Path, data: dict) -> list[str]:
    manifest_id = data.get("id")
    playbook_id = _playbook_id_from_manifest(path)
    if manifest_id != playbook_id:
        return [
            f"{path}: manifest id '{manifest_id}' must match filename stem '{playbook_id}'"
        ]
    pack_id = data.get("packId")
    pack_root = _pack_root(path)
    if pack_root and pack_id != pack_root.name.removesuffix(".pacs"):
        return [f"{path}: packId '{pack_id}' must match pack folder '{pack_root.name}'"]
    return []


def _resolve_from_manifest(manifest_path: Path, ref: str) -> Path:
    return (manifest_path.parent / ref).resolve()


def _validate_playbook_references(manifest_path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    pack_root = _pack_root(manifest_path)
    if pack_root is None:
        return errors

    for entry in data.get("requires") or []:
        if not isinstance(entry, dict):
            continue
        workflow = entry.get("workflow")
        if not workflow:
            continue
        workflow_ref = workflow if workflow.endswith(".md") else f"{workflow}.md"
        target = _resolve_from_manifest(manifest_path, workflow_ref)
        if not target.is_file():
            errors.append(f"{manifest_path}: missing workflow file: {workflow_ref}")

    for entry in data.get("uses") or []:
        if not isinstance(entry, dict):
            continue
        skill = entry.get("skill")
        if not skill:
            continue
        skill_md = _resolve_from_manifest(manifest_path, skill) / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{manifest_path}: missing skill: {skill}/SKILL.md")

    for entry in data.get("overlays") or []:
        if not isinstance(entry, dict):
            continue
        overlay_path = entry.get("path")
        if not overlay_path:
            continue
        if overlay_path.startswith("overlays/") or "/overlays/" in overlay_path.replace("\\", "/"):
            errors.append(
                f"{manifest_path}: overlay must live under layer2-overlays/, not playbook overlays/: {overlay_path}"
            )
        target = _resolve_from_manifest(manifest_path, overlay_path)
        try:
            target.relative_to((pack_root / "layer2-overlays").resolve())
        except ValueError:
            errors.append(
                f"{manifest_path}: overlay path must resolve under layer2-overlays/: {overlay_path}"
            )
            continue
        if not target.is_file():
            errors.append(f"{manifest_path}: missing overlay file: {overlay_path}")

    contract = (data.get("outputs") or {}).get("primary", {}).get("contract")
    if contract:
        target = (pack_root / contract).resolve()
        if not target.is_file():
            errors.append(f"{manifest_path}: missing output contract: {contract}")

    return errors


def _validate_pack_index(pack_path: Path, data: dict, playbook_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    pack_root = pack_path.parent
    declared = data.get("playbooks") or []
    if not isinstance(declared, list):
        return errors

    found_ids = {
        _playbook_id_from_manifest(p)
        for p in playbook_paths
        if _pack_root(p) == pack_root and p.name != "playbook.pacs.yaml"
    }
    declared_set = set(declared)

    for playbook_id in declared:
        manifest = pack_root / "layer3-playbooks" / playbook_id / f"{playbook_id}.pacs.yaml"
        if not manifest.is_file():
            errors.append(f"{pack_path}: playbooks lists '{playbook_id}' but missing {manifest.relative_to(pack_root)}")
        legacy = pack_root / "layer3-playbooks" / playbook_id / "playbook.pacs.yaml"
        if legacy.is_file():
            errors.append(f"{pack_path}: legacy manifest present: {legacy.relative_to(pack_root)}")

    for playbook_id in sorted(found_ids - declared_set):
        errors.append(f"{pack_path}: undeclared playbook manifest: layer3-playbooks/{playbook_id}/{playbook_id}.pacs.yaml")

    return errors


def _validate_pack_layout(pack_root: Path) -> list[str]:
    errors: list[str] = []

    legacy_playbook = sorted(pack_root.glob("layer3-playbooks/*/playbook.pacs.yaml"))
    for path in legacy_playbook:
        errors.append(f"{pack_root}: legacy manifest present: {path.relative_to(pack_root)}")

    playbook_overlay_dirs = sorted(pack_root.glob("layer3-playbooks/*/overlays"))
    for path in playbook_overlay_dirs:
        if path.is_dir() and any(path.iterdir()):
            errors.append(
                f"{pack_root}: overlays belong in layer2-overlays/, not {path.relative_to(pack_root)}/"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    yaml, Draft202012Validator = _load_deps()

    pack_validator = Draft202012Validator(_load_schema(PACK_SCHEMA))
    playbook_validator = Draft202012Validator(_load_schema(PLAYBOOK_SCHEMA))

    if argv:
        paths = [Path(p).resolve() for p in argv]
        pack_paths = [p for p in paths if _is_pack_manifest(p)]
        playbook_paths = [p for p in paths if _is_playbook_manifest(p)]
        unknown = [p for p in paths if p not in pack_paths and p not in playbook_paths]
        if unknown:
            print("Unknown manifest paths (expected pack.pacs.yaml or <playbook-id>.pacs.yaml):")
            for path in unknown:
                print(f"  {path}")
            return 2
        pack_roots = {_pack_root(p) for p in pack_paths if _pack_root(p)}
    else:
        pack_paths, playbook_paths = _discover_manifests(EXAMPLES_DIR)
        pack_roots = {p.parent for p in pack_paths}

    all_errors: list[str] = []
    for pack_root in sorted(pack_roots, key=lambda p: str(p)):
        if pack_root is not None:
            all_errors.extend(_validate_pack_layout(pack_root))

    for path in pack_paths:
        all_errors.extend(_validate_file(path, pack_validator, "pack"))
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                all_errors.extend(_validate_pack_index(path, data, playbook_paths))
        except Exception:
            pass

    for path in playbook_paths:
        all_errors.extend(_validate_playbook_path(path))
        all_errors.extend(_validate_file(path, playbook_validator, "playbook"))
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                all_errors.extend(_validate_playbook_id(path, data))
                all_errors.extend(_validate_playbook_references(path, data))
        except Exception:
            pass

    if all_errors:
        print("Manifest validation failed:")
        for line in all_errors:
            print(line)
        return 1

    print(
        f"OK: {len(pack_paths)} pack manifest(s), {len(playbook_paths)} playbook manifest(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
