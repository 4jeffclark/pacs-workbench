"""Portfolio period flows skill."""

from __future__ import annotations

from collections import defaultdict

from tc_lib.canonical import in_period, load_canonical, parse_float, work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "portfolio-period-flows")
    orders = load_canonical(args.datastore, "orders.csv")

    by_symbol: dict[str, dict[str, float]] = defaultdict(lambda: {"buy": 0.0, "sell": 0.0})
    for row in orders:
        if row.get("Status", "").lower() not in ("filled", "executed", "complete"):
            continue
        trade_date = row.get("TradeDate") or row.get("ActivityDate") or row.get("ExportedAtLocal", "")
        if not in_period(trade_date, args.period_start, args.period_end):
            continue
        sym = (row.get("Symbol") or "").upper()
        side = (row.get("Side") or "").lower()
        qty = parse_float(row.get("FillQuantity") or row.get("Quantity"))
        price = parse_float(row.get("FillPrice") or row.get("OrderPrice"))
        notional = abs(qty * price)
        if "buy" in side:
            by_symbol[sym]["buy"] += notional
        elif "sell" in side:
            by_symbol[sym]["sell"] += notional

    rows = []
    for sym, flows in sorted(by_symbol.items()):
        rows.append(
            {
                "Symbol": sym,
                "BuyNotional": f"{flows['buy']:.2f}",
                "SellNotional": f"{flows['sell']:.2f}",
                "NetNotional": f"{flows['buy'] - flows['sell']:.2f}",
            }
        )

    path = write_csv(
        out / "PeriodFlows.csv",
        ["Symbol", "BuyNotional", "SellNotional", "NetNotional"],
        rows,
    )
    return SkillResult(
        skill="portfolio-period-flows",
        status="ok",
        artifacts=[str(path)],
        metrics={"symbolCount": len(rows)},
        messages=["Wrote period flow rollups"],
    )
