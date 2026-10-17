# Backend / Reliability (opt-in)
- Map current data flows, invariants, side effects, retries and recovery procedures before editing.
- Use atomic boundaries, documented idempotency keys, explicit state machines, outbox patterns where justified, bounded retries and actionable observability.
- For money or irreversible effects, never treat tests alone as proof of production safety; require verification and safe rollout.
- Inspect existing implementation and production failure evidence first. No speculative replacements.
