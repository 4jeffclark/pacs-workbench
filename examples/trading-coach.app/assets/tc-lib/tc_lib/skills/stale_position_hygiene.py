"""Stale position hygiene skill."""

from __future__ import annotations

import json

from tc_lib.canonical import load_canonical, parse_float, work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "stale-position-hygiene")
    if not args.symbol:
        return SkillResult(skill="stale-position-hygiene", status="error", messages=["--symbol is required"])

    sym = args.symbol.upper()
    positions = [r for r in load_canonical(args.datastore, "positions_lot_level.csv") if (r.get("Symbol") or "").upper() == sym]
    mv = sum(parse_float(r.get("MarketValue") or r.get("CurrentValue")) for r in positions)

    weights_path = work_dir(args.workspace, "period-weight-reconstruction") / "boundary-weights.json"
    weight_pct = 0.0
    if weights_path.is_file():
        weights = json.loads(weights_path.read_text(encoding="utf-8")).get("symbolWeightsPct", {})
        weight_pct = float(weights.get(sym, 0.0))

    rows = [
        {"Check": "positionRowCount", "Value": str(len(positions))},
        {"Check": "marketValue", "Value": f"{mv:.2f}"},
        {"Check": "portfolioWeightPct", "Value": f"{weight_pct:.4f}"},
        {"Check": "staleRiskFlag", "Value": "review" if weight_pct > 5 else "low"},
    ]
    path = write_csv(out / f"{sym}-stale-hygiene.csv", ["Check", "Value"], rows)
    return SkillResult(
        skill="stale-position-hygiene",
        status="ok",
        artifacts=[str(path)],
        messages=["Wrote stale hygiene facts; evaluation overlay handles hold/exit judgment"],
    )
