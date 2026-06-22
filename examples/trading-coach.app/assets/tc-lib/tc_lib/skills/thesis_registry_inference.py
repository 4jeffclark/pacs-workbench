"""Thesis registry inference skill."""

from __future__ import annotations

import csv
from pathlib import Path

from tc_lib.canonical import work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "thesis-registry-inference")
    base = args.input_dir or work_dir(args.workspace, "theme-map-inference")
    theme_reg = _read_csv(base / "ThemeRegistry.csv")
    theme_map = _read_csv(base / "ThemeMap.csv")

    if not theme_map:
        return SkillResult(
            skill="thesis-registry-inference",
            status="error",
            messages=["ThemeMap.csv not found; run theme-map-inference first"],
        )

    registry = []
    assignment = []
    for i, theme in enumerate(theme_reg, start=1):
        tid = theme.get("ThemeId", f"thesis-{i:02d}")
        thesis_id = f"thesis-{i:02d}"
        registry.append(
            {
                "ThesisId": thesis_id,
                "ThesisLabel": theme.get("ThemeLabel", tid),
                "ThesisStatement": f"Exposure cluster aligned to {theme.get('ThemeLabel', tid)}",
                "ParentThemeId": tid,
                "Status": "candidate",
                "Notes": "Agent should refine thesis statements",
            }
        )
        for row in theme_map:
            if row.get("ThemeId") == tid:
                assignment.append(
                    {
                        "Symbol": row.get("Symbol", ""),
                        "ThesisId": thesis_id,
                        "MappingConfidence": "low",
                        "PrimaryFlag": "true",
                        "Notes": "",
                    }
                )

    reg_path = write_csv(
        out / "ThesisRegistry.csv",
        ["ThesisId", "ThesisLabel", "ThesisStatement", "ParentThemeId", "Status", "Notes"],
        registry,
    )
    asn_path = write_csv(
        out / "ThesisAssignment.csv",
        ["Symbol", "ThesisId", "MappingConfidence", "PrimaryFlag", "Notes"],
        assignment,
    )
    return SkillResult(
        skill="thesis-registry-inference",
        status="ok",
        artifacts=[str(reg_path), str(asn_path)],
        metrics={"thesisCount": len(registry)},
        messages=["Wrote candidate thesis registry; route to thesis-registry-confirmation"],
    )
