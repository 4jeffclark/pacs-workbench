"""Period weight reconstruction skill."""

from __future__ import annotations

import json

from tc_lib.canonical import load_canonical, parse_float, work_dir, ymd_to_iso
from tc_lib.cli import SkillArgs, SkillResult


def _mv_by_symbol(positions: list[dict[str, str]]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for row in positions:
        sym = (row.get("Symbol") or "").strip().upper()
        if not sym or sym in ("--", "PORTFOLIO ANALYSIS"):
            continue
        mv = parse_float(row.get("MarketValue") or row.get("CurrentValue") or row.get("Value"))
        totals[sym] = totals.get(sym, 0.0) + mv
    return totals


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "period-weight-reconstruction")
    positions = load_canonical(args.datastore, "positions_lot_level.csv")
    balances = load_canonical(args.datastore, "balances.csv")

    mv = _mv_by_symbol(positions)
    total_mv = sum(mv.values()) or 1.0
    weights = {sym: (val / total_mv) * 100.0 for sym, val in mv.items()}

    live_value = sum(parse_float(b.get("LiveAccountValue")) for b in balances)
    liquidity_syms = {s for s, w in weights.items() if s.endswith("XX") or s in ("SPAXX", "FDRXX")}
    liquidity_mv = sum(mv.get(s, 0.0) for s in liquidity_syms)
    liquidity_pct = (liquidity_mv / total_mv * 100.0) if total_mv else 0.0

    payload = {
        "analysisPeriodStart": args.period_start,
        "analysisPeriodEnd": args.period_end,
        "periodStartWeightSource": "observed_snapshot" if positions else "unavailable",
        "periodEndWeightSource": "observed_snapshot" if positions else "unavailable",
        "totalLiveAccountValue": live_value,
        "investedMarketValue": total_mv - liquidity_mv,
        "liquidityMarketValue": liquidity_mv,
        "liquidityPercent": round(liquidity_pct, 4),
        "symbolWeightsPct": weights,
    }

    path = out / "boundary-weights.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return SkillResult(
        skill="period-weight-reconstruction",
        status="ok",
        artifacts=[str(path)],
        metrics={"symbolCount": len(weights), "liquidityPercent": liquidity_pct},
        messages=["Wrote boundary weight reconstruction JSON; agent should validate against contract"],
    )
