"""Portfolio liquidity analysis skill."""

from __future__ import annotations

import json

from tc_lib.canonical import load_canonical, parse_float, work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult

CASH_EQUIV = {"SPAXX", "FDRXX", "VMFXX", "SWVXX", "BIL", "SGOV", "SHV"}


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "portfolio-liquidity-analysis")
    positions = load_canonical(args.datastore, "positions_lot_level.csv")
    cash = load_canonical(args.datastore, "cash.csv")

    rows = []
    for row in cash:
        rows.append(
            {
                "Component": "broker_cash",
                "Symbol": row.get("CashConcept", "Cash"),
                "Account": row.get("AccountLabel", ""),
                "PeriodStartMarketValue": "",
                "PeriodEndMarketValue": row.get("Amount", ""),
                "PeriodChangeMarketValue": "",
                "LiquidityRole": "broker_cash",
                "InstrumentType": "Cash",
            }
        )

    for row in positions:
        sym = (row.get("Symbol") or "").upper()
        role = "cash_equivalent" if sym in CASH_EQUIV else "invested"
        mv = parse_float(row.get("MarketValue") or row.get("CurrentValue"))
        rows.append(
            {
                "Component": "position",
                "Symbol": sym,
                "Account": row.get("AccountLabel", ""),
                "PeriodStartMarketValue": "",
                "PeriodEndMarketValue": f"{mv:.2f}",
                "PeriodChangeMarketValue": "",
                "LiquidityRole": role,
                "InstrumentType": row.get("AssetClass", "Equity"),
            }
        )

    path = write_csv(
        out / "LiquidityBreakdown.csv",
        [
            "Component",
            "Symbol",
            "Account",
            "PeriodStartMarketValue",
            "PeriodEndMarketValue",
            "PeriodChangeMarketValue",
            "LiquidityRole",
            "InstrumentType",
        ],
        rows,
    )
    return SkillResult(
        skill="portfolio-liquidity-analysis",
        status="ok",
        artifacts=[str(path)],
        metrics={"rowCount": len(rows)},
        messages=["Wrote LiquidityBreakdown.csv"],
    )
