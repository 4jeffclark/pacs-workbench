"""Event trade context skill."""

from __future__ import annotations

from tc_lib.canonical import work_dir, ymd_to_iso
from tc_lib.cli import SkillArgs, SkillResult


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "event-trade-context")
    sym = (args.symbol or "SYMBOL").upper()
    start = ymd_to_iso(args.period_start) or "TBD"
    end = ymd_to_iso(args.period_end) or "TBD"

    content = f"""# Event Trade Context — {sym}

Event window: {start} to {end}

## Agent checklist

1. Document event terms, reception, and lock-up where applicable.
2. Reconstruct allocation, entry, and exit orders for {sym}.
3. Compare trade path to market movement factually.
4. Defer sizing/timing quality judgments to evaluation overlay when active.

## Order reconstruction notes

_Agent links to symbol order exports and timeline._

## Citations

_Agent adds sources for event facts._
"""
    path = out / f"{sym}-event-context.md"
    path.write_text(content, encoding="utf-8")
    return SkillResult(
        skill="event-trade-context",
        status="ok",
        artifacts=[str(path)],
        messages=[f"Wrote event context template for {sym}"],
    )
