# Proposed personal Codex engineering rules

> **Proposal only.** Not active until deliberately installed as `~/.codex/AGENTS.md`. Review against current rules and project-specific requirements first.

## Working principle
Solve the actual user problem with a focused, maintainable change. Review nearby code, documentation, contracts, tests, and deployment impact before implementation.

## Scope
- Preserve existing behavior and contracts unless the task explicitly requires a change.
- Prefer small diffs; avoid unrelated formatting, refactors, renames and new dependencies.
- When the task is complex or risky, briefly state the approach, assumptions and failure modes before implementation. Do not impose a six-step written ritual for trivial work.
- For every completed authorized change, create a focused commit and clearly report what it contains. Preserve project and employer-specific approval restrictions. Do not push, deploy, migrate production data, or perform irreversible actions without separate appropriate authorization.
- When a meaningful change is delivered, update the reader-facing RELEASE_NOTES.md (or its approved equivalent) in plain everyday English, explaining the change, why it matters, and what remains unavailable. Keep implementation details in a separate technical report.

## Code quality
- For TypeScript, use meaningful types, narrow error handling and runtime validation at trust boundaries. Avoid `any` and unsafe assertions.
- Prefer clear ownership, functions of understandable size, and composable interfaces over clever abstractions.
- Preserve existing library/framework conventions unless change is justified.
- For UI work, verify accessibility, responsive behavior, empty/loading/error states, and the project's theme patterns.

## Reliability, performance and security
- Model failures explicitly: nulls, empty responses, retries, timeouts, concurrency, stale state and lost network access.
- Keep authorization on server-side boundaries; validate inputs and don't leak sensitive information.
- For databases, consider indexes, pagination, N+1 patterns, query selectivity and transaction boundaries.
- Treat payments, webhooks, retries and external side effects as higher-risk: idempotency, state-transition invariants, exact money, replay prevention and auditability.
- Use measurements and actual evidence when diagnosing regressions, not guesses.

## Verification
- Run relevant targeted automated checks when feasible, and report each command and outcome. Run broader suites at integration or release boundaries.
- Never weaken tests or suppress an important failure simply to report success.
- Distinguish **automated tests executed**, **manual scenarios awaiting owner verification**, **deployment evidence**, and **production evidence**.
- A local test or CI check is not proof of successful production behavior.
- Provide repeatable manual acceptance steps when the user owns UI/end-to-end sign-off.

## Communication
- Keep replies practical. Report: summary, changed files, checks/results, unresolved risks and next step.
- If blocked by missing access or environment, state exactly what was and wasn't verified.
- Explicitly flag suspected repeat failure classes and recommend a durable rule when appropriate.

## Scope exceptions
Project instructions prevail on business context and workflows unless a higher-priority safety restriction applies. Never copy confidential project instructions or credentials into a personal configuration repository.
