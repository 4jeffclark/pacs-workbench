"""Evaluation entry interview skill."""

from __future__ import annotations

from tc_lib.canonical import work_dir
from tc_lib.cli import SkillArgs, SkillResult
from tc_lib.skills._confirm import write_review_template


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "evaluation-entry-interview")
    path = write_review_template(
        out / "Interview.md",
        "Evaluation Entry Interview",
        [
            "What outcome are you optimizing for in this review?",
            "Which positions or themes need the most attention?",
            "Any constraints on recommendations?",
        ],
    )
    return SkillResult(
        skill="evaluation-entry-interview",
        status="ok",
        artifacts=[str(path)],
        messages=["Prepared entry interview template; agent conducts Q&A and records verbatim responses"],
    )
