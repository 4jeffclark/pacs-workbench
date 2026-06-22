---
name: portfolio-period-flows
description: TradingCoach skill: portfolio-period-flows
sourceCorpus:
  repository: trading-coach
  path: capabilities/portfolio-period-flows/
  readOnly: true
metadata:
  legacyCapabilityKind: analyze
---

1. Filter filled orders to analysis period
2. Aggregate by symbol and mapped thesis/category
3. Feed `portfolio-evolution` and Appendix B order tables

## Used by

- `layer3-playbooks/aggregate-state-review`