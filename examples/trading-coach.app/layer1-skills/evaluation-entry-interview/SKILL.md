---
name: evaluation-entry-interview
description: TradingCoach skill: evaluation-entry-interview
sourceCorpus:
  repository: trading-coach
  path: capabilities/evaluation-entry-interview/
  readOnly: true
metadata:
  legacyCapabilityKind: interact
---

1. Run only after Input Discovery, map confirmation (when applicable), and factual market context for the playbook
2. Ask targeted questions per active overlay (portfolio evaluation, rebalancing, risk, trade lifecycle, etc.)
3. Preserve complete Q&A verbatim
4. Store in `Interview.md` and embed in `Report.md` Appendix A
5. After completion say: `Interview complete. Generating report.`

Portfolio-specific themes when `aggregate-state-review`: see [overlays/portfolio-evaluation.md](../playbooks/aggregate-state-review/overlays/portfolio-evaluation.md).

## Outputs

- `Interview.md`
- Gate: `entry-interview-complete`

## Used by

- Evaluation overlays on portfolio, trade, and activity playbooks