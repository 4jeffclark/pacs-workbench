"""Portfolio weights table skill."""

from __future__ import annotations

import json
from pathlib import Path

from tc_lib.canonical import work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "portfolio-weights-table")
    weights_path = work_dir(args.workspace, "period-weight-reconstruction") / "boundary-weights.json"
    weights: dict[str, float] = {}
    if weights_path.is_file():
        payload = json.loads(weights_path.read_text(encoding="utf-8"))
        weights = payload.get("symbolWeightsPct", {})

    thematic = args.thematic if args.thematic is not None else True
    if thematic:
        fname = "ThesisExposure.csv"
        fields = ["ThesisId", "ExposurePct", "Symbol", "Notes"]
        rows = [{"ThesisId": sym, "ExposurePct": f"{pct:.4f}", "Symbol": sym, "Notes": ""} for sym, pct in weights.items()]
    else:
        fname = "CategoryExposure.csv"
        fields = ["Category", "ExposurePct", "Symbol", "Notes"]
        rows = [{"Category": sym, "ExposurePct": f"{pct:.4f}", "Symbol": sym, "Notes": ""} for sym, pct in weights.items()]

    path = write_csv(out / fname, fields, rows)
    bucket = write_csv(
        out / "GenericBucketExposure.csv",
        ["Bucket", "ExposurePct"],
        [{"Bucket": "Invested", "ExposurePct": f"{sum(weights.values()):.4f}"}],
    )
    return SkillResult(
        skill="portfolio-weights-table",
        status="ok",
        artifacts=[str(path), str(bucket)],
        messages=["Wrote exposure tables; agent embeds Section 3 and Figure 1 in Report.md"],
    )
