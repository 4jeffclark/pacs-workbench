"""Trading activity analysis skill."""

from __future__ import annotations

from collections import defaultdict

from tc_lib.canonical import in_period, load_canonical, parse_float, work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "trading-activity-analysis")
    orders = load_canonical(args.datastore, "orders.csv")

    filled = []
    pnl_proxy = 0.0
    wins = 0
    losses = 0
    daily: dict[str, float] = defaultdict(float)
    by_symbol: dict[str, float] = defaultdict(float)

    for row in orders:
        if row.get("Status", "").lower() not in ("filled", "executed", "complete"):
            continue
        d = (row.get("TradeDate") or row.get("ActivityDate") or "")[:10]
        if not in_period(d, args.period_start, args.period_end):
            continue
        sym = (row.get("Symbol") or "").upper()
        side = (row.get("Side") or "").lower()
        qty = parse_float(row.get("FillQuantity") or row.get("Quantity"))
        price = parse_float(row.get("FillPrice") or row.get("OrderPrice"))
        notional = qty * price
        signed = notional if "buy" in side else -notional
        pnl_proxy += signed
        daily[d] += signed
        by_symbol[sym] += signed
        if signed >= 0:
            wins += 1
        else:
            losses += 1
        filled.append(row)

    metrics = [
        {"Metric": "filledOrderCount", "Value": str(len(filled))},
        {"Metric": "netNotionalProxy", "Value": f"{pnl_proxy:.2f}"},
        {"Metric": "winCount", "Value": str(wins)},
        {"Metric": "lossCount", "Value": str(losses)},
    ]
    met_path = write_csv(out / "Metrics.csv", ["Metric", "Value"], metrics)
    daily_rows = [{"Date": d, "NetNotional": f"{v:.2f}"} for d, v in sorted(daily.items())]
    daily_path = write_csv(out / "DailyRollup.csv", ["Date", "NetNotional"], daily_rows)
    sym_rows = [{"Symbol": s, "NetNotional": f"{v:.2f}"} for s, v in sorted(by_symbol.items(), key=lambda x: -abs(x[1]))]
    sym_path = write_csv(out / "SymbolRollup.csv", ["Symbol", "NetNotional"], sym_rows)

    return SkillResult(
        skill="trading-activity-analysis",
        status="ok",
        artifacts=[str(met_path), str(daily_path), str(sym_path)],
        messages=["Wrote trading metrics; agent completes market context narrative"],
    )
