#!/usr/bin/env python3
"""Baseline agentskills.io directory shape for all skills under a pack instance."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = REPO_ROOT / "examples" / "trading-coach.app"
SKILLS_ROOT_NAME = "layer1-skills"

SCRIPTS_README = """# Scripts

Executable code for this skill per [agentskills.io](https://agentskills.io/specification).

APP skills are true Agent Skills. When this directory contains scripts, `SKILL.md` instructs the agent to run them using paths **relative to this skill directory** (for example `python3 scripts/example.py`).

See `docs/app-skills.md` in the [AgentPlaybookPack](https://github.com/4jeffclark/agent-playbook-pack) standards repo.

{status}
"""

SCRIPTS_SECTION_NONE = """## Scripts

No bundled scripts. Follow the procedure above. Scripts may be added under `scripts/` per [agentskills.io](https://agentskills.io/specification).
"""

REFERENCES_README = """# References

Optional reference material for this skill per [agentskills.io](https://agentskills.io/specification).

Load files from this directory on demand when `SKILL.md` points here. Prefer pack `contracts/` for durable cross-skill rules.
"""


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---\n"):
        return {}, "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, "", text
    raw = text[4:end]
    body = text[end + 5 :]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            fields[key.strip()] = val.strip()
    return fields, raw, body


def normalize_frontmatter(skill_id: str, raw: str) -> str:
    """Convert to agentskills.io-valid frontmatter (metadata string values only)."""
    lines = raw.splitlines()
    meta: dict[str, str] = {}
    top: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("sourceCorpus:"):
            i += 1
            repo = path = ""
            while i < len(lines) and lines[i].startswith("  "):
                part = lines[i].strip()
                if part.startswith("repository:"):
                    repo = part.split(":", 1)[1].strip()
                elif part.startswith("path:"):
                    path = part.split(":", 1)[1].strip()
                i += 1
            if repo:
                meta["sourceRepository"] = repo
            if path:
                meta["sourcePath"] = path.rstrip("/")
            continue
        if line.startswith("metadata:"):
            i += 1
            while i < len(lines) and lines[i].startswith("  "):
                part = lines[i].strip()
                if ":" in part:
                    k, v = part.split(":", 1)
                    meta[k.strip()] = v.strip()
                i += 1
            continue
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            top[k.strip()] = v.strip()
        i += 1

    if "legacyCapabilityKind" in top:
        meta["legacyCapabilityKind"] = top.pop("legacyCapabilityKind")

    name = top.get("name", skill_id)
    description = top.get("description", f"TradingCoach skill: {skill_id}")
    out = [f"name: {name}", f"description: {description}"]
    for key in ("license", "compatibility"):
        if key in top:
            out.append(f"{key}: {top[key]}")
    if meta:
        out.append("metadata:")
        for k, v in sorted(meta.items()):
            out.append(f"  {k}: {v}")
    return "\n".join(out)


def ensure_scripts_section(body: str) -> str:
    if re.search(r"^## Scripts\s*$", body, re.MULTILINE):
        return body
    insert_before = re.search(r"^## (Outputs|Used by)\s*$", body, re.MULTILINE)
    section = SCRIPTS_SECTION_NONE + "\n"
    if insert_before:
        pos = insert_before.start()
        return body[:pos] + section + body[pos:]
    return body.rstrip() + "\n\n" + section


def baseline_skill(skill_dir: Path) -> None:
    skill_id = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return

    text = skill_md.read_text(encoding="utf-8")
    fields, raw, body = parse_frontmatter(text)
    if raw:
        new_fm = normalize_frontmatter(skill_id, raw)
        body = ensure_scripts_section(body)
        skill_md.write_text(f"---\n{new_fm}\n---\n\n{body.lstrip()}", encoding="utf-8")

    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    scripts_readme = scripts_dir / "README.md"
    has_scripts = any(
        p.is_file() and p.name != "README.md" for p in scripts_dir.iterdir()
    )
    status = (
        "Bundled scripts are listed in `SKILL.md`."
        if has_scripts
        else "No bundled scripts yet. `SKILL.md` procedure is authoritative."
    )
    scripts_readme.write_text(SCRIPTS_README.format(status=status), encoding="utf-8")

    refs_dir = skill_dir / "references"
    refs_dir.mkdir(exist_ok=True)
    refs_readme = refs_dir / "README.md"
    if not refs_readme.exists():
        refs_readme.write_text(REFERENCES_README, encoding="utf-8")


def baseline_pack(pack_root: Path) -> None:
    skills_root = pack_root / SKILLS_ROOT_NAME
    if not skills_root.is_dir():
        raise SystemExit(f"No {SKILLS_ROOT_NAME}/ under {pack_root}")
    count = 0
    for skill_dir in sorted(skills_root.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            baseline_skill(skill_dir)
            count += 1
    print(f"Baselined {count} skills under {skills_root}")


def main() -> None:
    baseline_pack(DEFAULT_PACK)


if __name__ == "__main__":
    main()
