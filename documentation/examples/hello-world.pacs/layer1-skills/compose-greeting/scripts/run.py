#!/usr/bin/env python3
"""Hello World PACS skill: compose-greeting. See SKILL.md."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose a Hello World greeting.")
    parser.add_argument("--recipient", default="World", help="Name to greet")
    parser.add_argument(
        "--datastore",
        help="Bound user datastore path (accepted per PACS script interface; unused by this skill)",
    )
    parser.add_argument("--workspace", required=True, help="Agent workspace directory")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    greeting = f"Hello, {args.recipient}!"
    (workspace / "greeting.txt").write_text(greeting + "\n", encoding="utf-8")

    result = {
        "skill": "compose-greeting",
        "greeting": greeting,
        "recipient": args.recipient,
        "completedAt": datetime.now(timezone.utc).isoformat(),
    }
    (workspace / "skill-result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    print(greeting)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
