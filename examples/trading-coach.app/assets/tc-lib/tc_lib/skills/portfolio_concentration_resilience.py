"""Portfolio concentration resilience skill."""

from __future__ import annotations

import json

from tc_lib.canonical import work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def _hhi(weights: dict[str, float]) -> float:
    if not weights:
        return 0.0
    return sum((w / 100.0) ** 2 for w in weights.values())


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "portfolio-concentration-resilience")
    weights_path = work_dir(args.workspace, "period-weight-reconstruction") / "boundary-weights.json"
    weights: dict[str, float] = {}
    if weights_path.is_file():
        weights = json.loads(weights_path.read_text(encoding="utf-8")).get("symbolWeightsPct", {})

    hhi = _hhi(weights)
    rows = [
        {"Metric": "symbolHHI", "Value": f"{hhi:.6f}"},
        {"Metric": "largestWeightPct", "Value": f"{max(weights.values()) if weights else 0:.4f}"},
        {"Metric": "symbolCount", "Value": str(len(weights))},
    ]
    path = write_csv(out / "ConcentrationMetrics.csv", ["Metric", "Value"], rows)
    return SkillResult(
        skill="portfolio-concentration-resilience",
        status="ok",
        artifacts=[str(path)],
        metrics={"symbolHHI": hhi},
        messages=["Wrote concentration metrics; agent completes scenario narrative"],
    )
