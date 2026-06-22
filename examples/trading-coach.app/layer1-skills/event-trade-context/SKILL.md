---
name: event-trade-context
description: TradingCoach skill: event-trade-context
sourceCorpus:
  repository: trading-coach
  path: capabilities/event-trade-context/
  readOnly: true
metadata:
  legacyCapabilityKind: retrieve
---

1. Document event window, offering terms, market reception, lock-up and liquidity constraints when applicable
2. Reconstruct allocation, entry, and exit orders for the symbol
3. Compare outcome to event-day and post-event market path
4. Evaluation overlay: judgment on sizing, timing, and risk management for the event

## Used by

- `layer3-playbooks/unit-decision-review`