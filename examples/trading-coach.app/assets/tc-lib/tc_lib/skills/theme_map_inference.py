"""Theme map inference skill."""

from __future__ import annotations

import csv
from pathlib import Path

from tc_lib.canonical import work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def _load_holdings_map(args: SkillArgs) -> list[dict[str, str]]:
    candidates = [
        args.input_dir / "HoldingsMap.csv" if args.input_dir else None,
        work_dir(args.workspace, "holdings-standards-map") / "HoldingsMap.csv",
    ]
    for path in candidates:
        if path and path.is_file():
            with path.open(encoding="utf-8-sig", newline="") as f:
                return list(csv.DictReader(f))
    return []


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "theme-map-inference")
    holdings = _load_holdings_map(args)
    if not holdings:
        return SkillResult(
            skill="theme-map-inference",
            status="error",
            messages=["HoldingsMap.csv not found; run holdings-standards-map first or pass --input-dir"],
        )

    groups: dict[str, list[str]] = {}
    for row in holdings:
        sym = row.get("Symbol", "")
        sector = row.get("GICSSector") or row.get("AssetSubclass") or row.get("AssetClass") or "Residual"
        groups.setdefault(sector, []).append(sym)

    registry = []
    theme_map = []
    for i, (label, syms) in enumerate(sorted(groups.items()), start=1):
        tid = f"theme-{i:02d}"
        registry.append(
            {
                "ThemeId": tid,
                "ThemeLabel": label[:64],
                "ThemeNamespace": "CUSTOM",
                "ExternalThemeCode": "",
                "ParentThemeGroup": "",
                "Description": f"Inferred group for {label}",
                "Status": "candidate",
            }
        )
        for sym in syms:
            if (holdings_map_row := next((h for h in holdings if h.get("Symbol") == sym), None)) and (
                holdings_map_row.get("LiquidityRole") in ("cash_equivalent", "broker_cash")
            ):
                continue
            theme_map.append(
                {
                    "Symbol": sym,
                    "ThemeId": tid,
                    "MappingConfidence": "low",
                    "PrimaryFlag": "true",
                    "Notes": "Agent should refine theme assignments",
                }
            )

    reg_path = write_csv(
        out / "ThemeRegistry.csv",
        ["ThemeId", "ThemeLabel", "ThemeNamespace", "ExternalThemeCode", "ParentThemeGroup", "Description", "Status"],
        registry,
    )
    map_path = write_csv(
        out / "ThemeMap.csv",
        ["Symbol", "ThemeId", "MappingConfidence", "PrimaryFlag", "Notes"],
        theme_map,
    )
    return SkillResult(
        skill="theme-map-inference",
        status="ok",
        artifacts=[str(reg_path), str(map_path)],
        metrics={"themeCount": len(registry), "mappedSymbols": len(theme_map)},
        messages=["Wrote candidate theme registry; route to theme-map-confirmation"],
    )
