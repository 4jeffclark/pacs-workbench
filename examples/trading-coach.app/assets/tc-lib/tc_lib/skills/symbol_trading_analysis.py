"""Symbol trading analysis skill."""

from __future__ import annotations

from tc_lib.canonical import in_period, load_canonical, parse_float, work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "symbol-trading-analysis")
    if not args.symbol:
        return SkillResult(skill="symbol-trading-analysis", status="error", messages=["--symbol is required"])

    sym = args.symbol.upper()
    orders = load_canonical(args.datastore, "orders.csv")
    rows = []
    for row in orders:
        if (row.get("Symbol") or "").upper() != sym:
            continue
        d = (row.get("TradeDate") or row.get("ActivityDate") or "")[:10]
        if not in_period(d, args.period_start, args.period_end):
            continue
        rows.append(
            {
                "TradeDate": d,
                "Side": row.get("Side", ""),
                "Quantity": row.get("FillQuantity") or row.get("Quantity", ""),
                "Price": row.get("FillPrice") or row.get("OrderPrice", ""),
                "Status": row.get("Status", ""),
                "Notional": f"{parse_float(row.get('FillQuantity') or row.get('Quantity')) * parse_float(row.get('FillPrice') or row.get('OrderPrice')):.2f}",
            }
        )

    path = write_csv(
        out / f"{sym}-orders.csv",
        ["TradeDate", "Side", "Quantity", "Price", "Status", "Notional"],
        rows,
    )
    return SkillResult(
        skill="symbol-trading-analysis",
        status="ok",
        artifacts=[str(path)],
        metrics={"orderCount": len(rows)},
        messages=[f"Wrote order timeline for {sym}; agent completes lifecycle narrative"],
    )
