"""Holdings standards map skill."""

from __future__ import annotations

from tc_lib.canonical import (
    load_canonical,
    parse_float,
    symbols_from_positions,
    work_dir,
    write_csv,
)
from tc_lib.cli import SkillArgs, SkillResult

CASH_SYMBOLS = {"SPAXX", "FDRXX", "VMFXX", "SWVXX", "BIL", "SGOV", "SHV"}


def _classify_symbol(sym: str) -> dict[str, str]:
    s = sym.upper()
    if s in CASH_SYMBOLS or s.endswith("XX") and len(s) <= 5:
        return {
            "AssetClass": "Cash",
            "AssetSubclass": "MoneyMarket",
            "GICSSector": "",
            "GICSIndustry": "",
            "StyleBucket": "Liquidity",
            "LiquidityRole": "cash_equivalent",
            "MappingConfidence": "medium",
            "MappingSource": "heuristic_script",
            "Notes": "Cash or money-market sleeve",
        }
    if len(s) > 10 or " " in s:
        return {
            "AssetClass": "Other",
            "AssetSubclass": "Unclassified",
            "GICSSector": "",
            "GICSIndustry": "",
            "StyleBucket": "",
            "LiquidityRole": "invested",
            "MappingConfidence": "low",
            "MappingSource": "heuristic_script",
            "Notes": "Review classification",
        }
    return {
        "AssetClass": "Equity",
        "AssetSubclass": "CommonStock",
        "GICSSector": "",
        "GICSIndustry": "",
        "StyleBucket": "",
        "LiquidityRole": "invested",
        "MappingConfidence": "low",
        "MappingSource": "heuristic_script",
        "Notes": "Agent should refine GICS and subclass",
    }


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "holdings-standards-map")
    positions = load_canonical(args.datastore, "positions_lot_level.csv")
    symbols = symbols_from_positions(positions)
    if not symbols:
        symbols = sorted({(r.get("Symbol") or "").upper() for r in load_canonical(args.datastore, "orders.csv") if r.get("Symbol")})

    rows = []
    for sym in symbols:
        row = {"Symbol": sym, **_classify_symbol(sym)}
        rows.append(row)

    path = write_csv(
        out / "HoldingsMap.csv",
        [
            "Symbol",
            "AssetClass",
            "AssetSubclass",
            "GICSSector",
            "GICSIndustry",
            "StyleBucket",
            "LiquidityRole",
            "MappingConfidence",
            "MappingSource",
            "Notes",
        ],
        rows,
    )
    return SkillResult(
        skill="holdings-standards-map",
        status="ok",
        artifacts=[str(path)],
        metrics={"symbolCount": len(rows)},
        messages=[f"Wrote HoldingsMap.csv with {len(rows)} symbols; agent must refine and confirm"],
    )
