# Learning protocol: turn experience into better rules

This repository stores **reviewable knowledge**, not automatic model training. Agents must fetch/read the relevant instructions each session; cross-tool enforcement and automatic synchronization are not guaranteed.

For a failure, useful implementation, review or benchmark:

1. Capture **observation** and evidence (sanitized). State whether observed locally, tested, documented or hypothesized.
2. Explain **cause**, user impact and alternatives.
3. Propose **rule**, written as an actionable instruction with an applicability condition and exception.
4. Select **scope**: shared/core (broadly reusable), category (e.g. 3D editor), project (e.g. Moatt), or temporary experiment.
5. Add **verification**: regression test, review check or measurable acceptance criterion.
6. Cross-check existing rules for contradictions, duplicates and overreach. Avoid turning one anecdote into a universal prohibition.
7. Commit a traceable change, document reason and affected projects; update consuming project pointers/adapters as appropriate.
8. Reassess after evidence accumulates; amend or retire poor rules.

Suggested note template:

```md
## YYYY-MM-DD — Short title
Scope: core | category | project
Status: proposed | validated | retired
Observed: ...
Evidence: ... (non-confidential)
Cause: ...
Rule: When ..., do ..., unless ...
Verification: ...
References: ...
```

Do not add unverified ideas directly to mandatory global rules. A link to a central rule library is not equivalent to active runtime instructions.
