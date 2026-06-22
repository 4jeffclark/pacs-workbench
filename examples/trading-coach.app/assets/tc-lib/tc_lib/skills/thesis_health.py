"""Thesis health skill."""

from __future__ import annotations

import csv
from pathlib import Path

from tc_lib.canonical import work_dir, write_csv
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "thesis-health")
    evo = work_dir(args.workspace, "portfolio-evolution") / "ThesisEvolution.csv"
    rows = []
    if evo.is_file():
        with evo.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                net = float(row.get("NetFlow", 0) or 0)
                rows.append(
                    {
                        "ThesisId": row.get("ThesisId", ""),
                        "MomentumScore": "0",
                        "RelativeStrengthScore": "0",
                        "VolatilityScore": "0",
                        "DrawdownScore": "0",
                        "CompositeHealth": "neutral" if net >= 0 else "watch",
                        "Notes": "Agent completes health scoring and Figure 2",
                    }
                )

    path = write_csv(
        out / "ThesisHealth.csv",
        [
            "ThesisId",
            "MomentumScore",
            "RelativeStrengthScore",
            "VolatilityScore",
            "DrawdownScore",
            "CompositeHealth",
            "Notes",
        ],
        rows,
    )
    return SkillResult(
        skill="thesis-health",
        status="ok",
        artifacts=[str(path)],
        messages=["Wrote ThesisHealth scaffold; agent completes scoring"],
    )
