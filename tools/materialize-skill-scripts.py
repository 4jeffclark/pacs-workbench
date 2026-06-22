#!/usr/bin/env python3
"""Write scripts/run.py and update SKILL.md Scripts sections for all pack skills."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "examples" / "trading-coach.app"
SKILLS = PACK / "layer1-skills"

SKILL_MODULES: dict[str, str] = {
    "datastore-inventory": "datastore_inventory",
    "holdings-standards-map": "holdings_standards_map",
    "theme-map-inference": "theme_map_inference",
    "thesis-registry-inference": "thesis_registry_inference",
    "period-weight-reconstruction": "period_weight_reconstruction",
    "portfolio-holdings-state": "portfolio_holdings_state",
    "portfolio-period-flows": "portfolio_period_flows",
    "portfolio-evolution": "portfolio_evolution",
    "portfolio-weights-table": "portfolio_weights_table",
    "portfolio-liquidity-analysis": "portfolio_liquidity_analysis",
    "thesis-health": "thesis_health",
    "portfolio-concentration-resilience": "portfolio_concentration_resilience",
    "market-environment": "market_environment",
    "holdings-map-confirmation": "holdings_map_confirmation",
    "theme-map-confirmation": "theme_map_confirmation",
    "thesis-registry-confirmation": "thesis_registry_confirmation",
    "evaluation-entry-interview": "evaluation_entry_interview",
    "exit-interview": "exit_interview",
    "trading-activity-analysis": "trading_activity_analysis",
    "symbol-trading-analysis": "symbol_trading_analysis",
    "stale-position-hygiene": "stale_position_hygiene",
    "event-trade-context": "event_trade_context",
    "source-profile-insights": "source_profile_insights",
}

RUN_PY = '''#!/usr/bin/env python3
"""TradingCoach skill: {skill_id}. See SKILL.md."""
from __future__ import annotations

import sys
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACK_ROOT / "assets" / "tc-lib"))

from tc_lib.cli import run_main  # noqa: E402
from tc_lib.skills.{module} import run  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(run_main("{skill_id}", run))
'''

SCRIPTS_README = """# Scripts

| Script | Purpose |
| --- | --- |
| `run.py` | Execute this skill; writes artifacts under `--workspace` and `skill-result.json` |

Requires **Python 3.11+** (stdlib only). Shared library: `../../assets/tc-lib/`.

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE"{extra_args}
```
"""

SCRIPT_SECTION = """
## Scripts

Run from this skill directory. Paths are relative to the skill root per [agentskills.io](https://agentskills.io/specification).

| Script | Purpose |
| --- | --- |
| `scripts/run.py` | Execute skill logic; writes workspace artifacts and `skill-result.json` |

```bash
python scripts/run.py --datastore "$USER_DATASTORE" --workspace "$AGENT_WORKSPACE"{extra_args}
```

Set `compatibility: Requires Python 3.11+` when the runtime must execute bundled scripts.
"""

EXTRA_ARGS: dict[str, str] = {
    "period-weight-reconstruction": ' --period-start YYYYMMDD --period-end YYYYMMDD',
    "portfolio-period-flows": ' --period-start YYYYMMDD --period-end YYYYMMDD',
    "portfolio-evolution": ' --period-start YYYYMMDD --period-end YYYYMMDD --thematic true',
    "portfolio-weights-table": ' --thematic true',
    "trading-activity-analysis": ' --period-start YYYYMMDD --period-end YYYYMMDD',
    "symbol-trading-analysis": ' --symbol SYMBOL --period-start YYYYMMDD --period-end YYYYMMDD',
    "stale-position-hygiene": ' --symbol SYMBOL',
    "event-trade-context": ' --symbol SYMBOL --period-start YYYYMMDD --period-end YYYYMMDD',
    "market-environment": ' --period-start YYYYMMDD --period-end YYYYMMDD',
    "theme-map-inference": ' --input-dir "$AGENT_WORKSPACE/holdings-standards-map"',
    "thesis-registry-inference": ' --input-dir "$AGENT_WORKSPACE/theme-map-inference"',
    "holdings-map-confirmation": ' --input-dir "$AGENT_WORKSPACE/holdings-standards-map"',
    "theme-map-confirmation": ' --input-dir "$AGENT_WORKSPACE/theme-map-inference"',
    "thesis-registry-confirmation": ' --input-dir "$AGENT_WORKSPACE/thesis-registry-inference"',
    "source-profile-insights": ' --evaluation false',
    "evaluation-entry-interview": ' --evaluation true',
    "exit-interview": ' --evaluation true',
}


def update_skill_md(skill_dir: Path, skill_id: str) -> None:
    path = skill_dir / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    extra = EXTRA_ARGS.get(skill_id, "")
    section = SCRIPT_SECTION.format(extra_args=extra)

    if re.search(r"^## Scripts\s*$", text, re.MULTILINE):
        text = re.sub(r"^## Scripts\n.*?(?=^## |\Z)", section.lstrip() + "\n", text, count=1, flags=re.MULTILINE | re.DOTALL)
    else:
        text = re.sub(r"(^## Outputs)", section + r"\1", text, count=1, flags=re.MULTILINE)

    if "compatibility:" not in text.split("---", 2)[1]:
        text = text.replace(
            f"name: {skill_id}\n",
            f"name: {skill_id}\ncompatibility: Requires Python 3.11+ when running bundled scripts\n",
            1,
        )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for skill_id, module in SKILL_MODULES.items():
        skill_dir = SKILLS / skill_id
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "run.py").write_text(RUN_PY.format(skill_id=skill_id, module=module), encoding="utf-8")
        extra = EXTRA_ARGS.get(skill_id, "")
        (scripts_dir / "README.md").write_text(SCRIPTS_README.format(extra_args=extra), encoding="utf-8")
        update_skill_md(skill_dir, skill_id)
        print(f"  {skill_id}")
    print(f"Materialized {len(SKILL_MODULES)} skill scripts under {SKILLS}")


if __name__ == "__main__":
    main()
