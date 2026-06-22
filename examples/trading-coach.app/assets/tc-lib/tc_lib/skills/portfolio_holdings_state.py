"""Portfolio holdings state skill."""

from __future__ import annotations

import json

from tc_lib.canonical import load_canonical, parse_float, work_dir
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "portfolio-holdings-state")
    positions = load_canonical(args.datastore, "positions_lot_level.csv")
    cash = load_canonical(args.datastore, "cash.csv")
    balances = load_canonical(args.datastore, "balances.csv")

    inventory = []
    for row in positions:
        sym = (row.get("Symbol") or "").strip()
        if not sym or sym in ("--", "Portfolio Analysis"):
            continue
        inventory.append(
            {
                "Symbol": sym,
                "AccountId": row.get("AccountId", ""),
                "Quantity": row.get("Quantity", ""),
                "MarketValue": row.get("MarketValue") or row.get("CurrentValue") or "",
                "AsOfLocal": row.get("AsOfLocal", ""),
            }
        )

    total_mv = sum(parse_float(r.get("MarketValue")) for r in inventory)
    payload = {
        "boundaryMarketValue": total_mv,
        "positionCount": len(inventory),
        "cashRowCount": len(cash),
        "balanceRowCount": len(balances),
        "positions": inventory,
    }
    path = out / "holdings-state.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return SkillResult(
        skill="portfolio-holdings-state",
        status="ok",
        artifacts=[str(path)],
        metrics={"positionCount": len(inventory), "boundaryMarketValue": total_mv},
        messages=["Wrote holdings state snapshot"],
    )
