"""Holdings map confirmation skill."""

from __future__ import annotations

from tc_lib.canonical import work_dir
from tc_lib.cli import SkillArgs, SkillResult
from tc_lib.skills._confirm import validate_csv, write_review_template

HOLDINGS_FIELDS = [
    "Symbol",
    "AssetClass",
    "AssetSubclass",
    "GICSSector",
    "GICSIndustry",
    "StyleBucket",
    "LiquidityRole",
    "MappingConfidence",
    "MappingSource",
    "Notes",
]


def run(args: SkillArgs) -> SkillResult:
    out = work_dir(args.workspace, "holdings-map-confirmation")
    src = (args.input_dir or work_dir(args.workspace, "holdings-standards-map")) / "HoldingsMap.csv"
    errors = validate_csv(src, HOLDINGS_FIELDS)

    low_conf = []
    if src.is_file():
        import csv

        with src.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if (row.get("MappingConfidence") or "").lower() in ("low", "") or not row.get("GICSSector"):
                    low_conf.append(row.get("Symbol", ""))

    review = write_review_template(
        out / "MappingDiscovery.md",
        "Holdings Map Confirmation",
        [
            "Confirm AssetClass and AssetSubclass groupings",
            "Resolve low-confidence rows: " + ", ".join(low_conf[:20]),
            "Confirm liquidity sleeves and any dual roles",
            "Explicit approval: Holdings map confirmed.",
        ],
    )

    status = "ok"
    msgs = errors or ["Prepared holdings confirmation session; await explicit user approval"]
    if errors:
        msgs = ["Validation warnings (agent must resolve before gate):"] + errors + msgs
    return SkillResult(
        skill="holdings-map-confirmation",
        status=status,
        artifacts=[str(review)] + ([str(src)] if src.is_file() else []),
        messages=msgs,
        metrics={"lowConfidenceSymbols": len(low_conf)},
    )
