"""CSV validation helpers for confirmation skills."""

from __future__ import annotations

import csv
from pathlib import Path


def validate_csv(path: Path, required_columns: list[str]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"Missing file: {path.name}"]
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        for col in required_columns:
            if col not in cols:
                errors.append(f"Missing column {col} in {path.name}")
        rows = list(reader)
    if not rows:
        errors.append(f"No data rows in {path.name}")
    return errors


def write_review_template(path: Path, title: str, items: list[str]) -> Path:
    lines = [f"# {title}", "", "## Review prompts", ""]
    for item in items:
        lines.append(f"- {item}")
    lines.extend(["", "## User responses", "", "_Agent records verbatim Q&A here._", ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
