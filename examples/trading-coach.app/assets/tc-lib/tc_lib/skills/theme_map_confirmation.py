"""Theme map confirmation skill."""

from __future__ import annotations

from tc_lib.canonical import work_dir
from tc_lib.cli import SkillArgs, SkillResult
from tc_lib.skills._confirm import validate_csv, write_review_template


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "theme-map-confirmation")
    base = args.input_dir or work_dir(args.workspace, "theme-map-inference")
    reg = base / "ThemeRegistry.csv"
    tmap = base / "ThemeMap.csv"
    errors = validate_csv(reg, ["ThemeId", "ThemeLabel", "ThemeNamespace", "Status"])
    errors += validate_csv(tmap, ["Symbol", "ThemeId", "MappingConfidence", "PrimaryFlag"])

    review = write_review_template(
        out / "MappingDiscovery.md",
        "Theme Map Confirmation",
        [
            "Review ThemeRegistry entries for merge/split/rename",
            "Confirm primary ThemeId per symbol",
            "Resolve residual unmapped symbols",
            "Explicit approval: Theme map confirmed.",
        ],
    )
    return SkillResult(
        skill="theme-map-confirmation",
        status="ok",
        artifacts=[str(review)],
        messages=errors or ["Prepared theme confirmation session"],
    )
