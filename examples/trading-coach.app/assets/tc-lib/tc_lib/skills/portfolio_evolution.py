"""Portfolio evolution skill."""

from __future__ import annotations

import csv
from pathlib import Path

from tc_lib.canonical import work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def _flows(args: SkillArgs) -> list[dict[str, str]]:
    path = work_dir(args.workspace, "portfolio-period-flows") / "PeriodFlows.csv"
    if args.input_dir:
        alt = args.input_dir / "PeriodFlows.csv"
        if alt.is_file():
            path = alt
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "portfolio-evolution")
    flows = _flows(args)
    thematic = args.thematic if args.thematic is not None else True

    if thematic:
        key_field, evo_name, rot_name = "ThesisId", "ThesisEvolution.csv", "ThesisRotationMatrix.csv"
        grouped: dict[str, dict[str, float]] = {}
        for row in flows:
            tid = row.get("Symbol", "unassigned")
            g = grouped.setdefault(tid, {"buy": 0.0, "sell": 0.0})
            g["buy"] += float(row.get("BuyNotional", 0) or 0)
            g["sell"] += float(row.get("SellNotional", 0) or 0)
        evo_rows = [
            {
                "ThesisId": k,
                "PeriodStartWeightPct": "",
                "PeriodEndWeightPct": "",
                "BuyNotional": f"{v['buy']:.2f}",
                "SellNotional": f"{v['sell']:.2f}",
                "NetFlow": f"{v['buy'] - v['sell']:.2f}",
                "GrossTurnover": f"{v['buy'] + v['sell']:.2f}",
            }
            for k, v in sorted(grouped.items())
        ]
        evo_fields = [
            "ThesisId",
            "PeriodStartWeightPct",
            "PeriodEndWeightPct",
            "BuyNotional",
            "SellNotional",
            "NetFlow",
            "GrossTurnover",
        ]
    else:
        evo_name, rot_name = "CategoryEvolution.csv", "CategoryRotationMatrix.csv"
        evo_fields = [
            "Category",
            "PeriodStartWeightPct",
            "PeriodEndWeightPct",
            "BuyNotional",
            "SellNotional",
            "NetFlow",
            "GrossTurnover",
        ]
        evo_rows = [
            {
                "Category": row.get("Symbol", ""),
                "PeriodStartWeightPct": "",
                "PeriodEndWeightPct": "",
                "BuyNotional": row.get("BuyNotional", ""),
                "SellNotional": row.get("SellNotional", ""),
                "NetFlow": row.get("NetNotional", ""),
                "GrossTurnover": f"{float(row.get('BuyNotional', 0) or 0) + float(row.get('SellNotional', 0) or 0):.2f}",
            }
            for row in flows
        ]

    evo_path = write_csv(out / evo_name, evo_fields, evo_rows)
    rot_path = write_csv(
        out / rot_name,
        ["FromId", "ToId", "FlowNotional", "Notes"],
        [],
    )
    return SkillResult(
        skill="portfolio-evolution",
        status="ok",
        artifacts=[str(evo_path), str(rot_path)],
        messages=["Wrote evolution CSVs; agent completes weights and rotation narrative"],
    )
