"""Market environment skill."""

from __future__ import annotations

from tc_lib.canonical import work_dir, ymd_to_iso
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "market-environment")
    start = ymd_to_iso(args.period_start) or "TBD"
    end = ymd_to_iso(args.period_end) or "TBD"

    content = f"""# Market Research Brief

Analysis window: {start} to {end}

## Agent checklist

1. Summarize index and sector regime for the confirmed window.
2. Note volatility and rates context factually.
3. Capture headline catalysts with full citations for Report Appendix C.
4. When `evaluation: false`, avoid coaching judgments.

## Citations (complete in Report Appendix C)

| Title | Publisher | Date | Locator |
| --- | --- | --- | --- |
| _Agent fills_ | | | |

## Working notes

_Agent expands this file during research._
"""
    path = out / "MarketResearch.md"
    path.write_text(content, encoding="utf-8")
    return SkillResult(
        skill="market-environment",
        status="ok",
        artifacts=[str(path)],
        messages=["Wrote MarketResearch.md template; agent completes research and citations"],
    )
