"""Thesis registry confirmation skill."""

from __future__ import annotations

from tc_lib.canonical import work_dir
from tc_lib.cli import SkillArgs, SkillResult
from tc_lib.skills._confirm import validate_csv, write_review_template


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "thesis-registry-confirmation")
    base = args.input_dir or work_dir(args.workspace, "thesis-registry-inference")
    reg = base / "ThesisRegistry.csv"
    asn = base / "ThesisAssignment.csv"
    errors = validate_csv(reg, ["ThesisId", "ThesisLabel", "ThesisStatement", "Status"])
    errors += validate_csv(asn, ["Symbol", "ThesisId", "MappingConfidence", "PrimaryFlag"])

    review = write_review_template(
        out / "MappingDiscovery.md",
        "Thesis Registry Confirmation",
        [
            "Merge/split/rename candidate theses",
            "Reassign uncovered symbols",
            "Close retired theses",
            "Explicit approval: Thesis registry confirmed.",
        ],
    )
    return SkillResult(
        skill="thesis-registry-confirmation",
        status="ok",
        artifacts=[str(review)],
        messages=errors or ["Prepared thesis confirmation session"],
    )
