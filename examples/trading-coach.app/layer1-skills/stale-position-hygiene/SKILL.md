---
name: stale-position-hygiene
description: TradingCoach skill: stale-position-hygiene
sourceCorpus:
  repository: trading-coach
  path: capabilities/stale-position-hygiene/
  readOnly: true
metadata:
  legacyCapabilityKind: validate
---

1. Establish hold duration, drawdown from peak, thesis drift vs original entry rationale
2. Compare position size to portfolio context when holdings data exists
3. Document stale-risk rules (max age, max drawdown, thesis refresh triggers)
4. Quantification: factual timeline and metrics only
5. Evaluation overlay: judgment on whether hold vs exit was sound

## Used by

- `layer3-playbooks/unit-decision-review`