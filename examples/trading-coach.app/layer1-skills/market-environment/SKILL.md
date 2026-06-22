---
name: market-environment
description: TradingCoach skill: market-environment
sourceCorpus:
  repository: trading-coach
  path: capabilities/market-environment/
  readOnly: true
metadata:
  legacyCapabilityKind: retrieve
---

1. Broad regime narrative across confirmed windows
2. When embedded in portfolio playbook: summary suitable for Report market sections
3. When standalone: full `environment-review` playbook depth
4. Write a working copy to `MarketResearch.md` for agents and tooling
5. **Embed full source citations in `Report.md` Appendix C** — title, publisher, date, URL or sufficient locator. Appendix C must be self-contained; do **not** end with a pointer to `MarketResearch.md`.
6. Body sections may summarize context; Appendix C holds the complete citation list.

When `evaluation: false`, describe context without coaching judgments.

## Outputs

- `MarketResearch.md`
- Report market context sections

## Used by

- `layer3-playbooks/aggregate-state-review` (embeds)
- `layer3-playbooks/environment-review` (full)
- `layer3-playbooks/unit-decision-review` (optional)