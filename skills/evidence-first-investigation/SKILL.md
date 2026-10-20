---
name: evidence-first-investigation
description: Investigate bugs, production incidents, regressions, ambiguous behavior and technical decisions through a falsifiable, evidence-led workflow before making conclusions.
---

# Evidence-first investigation

**Trigger:** A user asks to investigate, diagnose, debug, understand why, compare likely causes, assess a risky change, review an incident, or design a substantial fix. The user should simply ask in ordinary language. Do not require a ritual phrase, project ID, or command. For a trivial and already-established fix, use a proportionate lightweight version.

**Core loop:** Understand → Investigate → Gather evidence → Eliminate possibilities → Verify → Recommend → Learn.

## 1 — Understand the question
State the observed failure and the expected behavior, affected scope and environment, impact and urgency. Inspect the actual authorized repository and user-provided logs before building a theory. Separate observed facts from reports, guesses and desired outcomes. If a prerequisite is unavailable, label it.

## 2 — Investigate the system
Trace the relevant request, state transition, data owner, callers, dependencies, recent changes and failure boundaries. Identify where the behavior diverges. Prefer direct evidence from the code and system over generic debugging folklore. For private/employer systems, stay in approved tools; do not export code, internal architecture, credentials, user data or incident records to the personal AI repository.

## 3 — Gather evidence
Create a short evidence ledger:
- **Observation:** What actually happened, with environment and time where available.
- **Evidence:** Exact authorized test/log/code location, its relevance, and what it cannot establish.
- **Confidence:** Verified by direct observation, supported but incomplete, reported, or hypothetical.
- **Disconfirming check:** What would show the current theory is wrong?

Never claim that a stack trace, log screenshot, test pass or documentation confirms more than it does. Unknown should stay unknown; logs showing a generic error are not a root-cause explanation.

## 4 — Eliminate possibilities
List at least two plausible explanations when uncertainty is meaningful. For each, specify a discriminating test or observation; mark it **ruled out**, **still possible**, or **supported**. Reject only when contradictory evidence exists; lack of evidence is not disproof. Reevaluate after each check. Do not list elaborate alternatives when a deterministic reproduction already explains the problem.

## 5 — Verify
Before calling a cause *confirmed*, obtain direct, relevant evidence explaining the specific failure and exclude material alternatives (for example, reproduce under controlled conditions; trace the failing call and error; validate the request and data state). Check the fix against a failing-then-passing regression and important nearby behavior when implementation is authorized. Run the checks or clearly report they were not run. A proposed fix that merely sounds reasonable is not verification.

## 6 — Recommend
Make a decision at the correct confidence level:
- **Confirmed:** cause and mechanism directly established; cite evidence and actual verification.
- **Likely:** evidence favors a cause but meaningful gaps remain.
- **Unresolved:** identify exactly which check would decide, including the fastest authorized way to collect it.

Separate diagnosis from proposed changes. Explain the smallest practical solution, tradeoffs, regression risks and validation plan. If the user asks for *diagnosis only*, do not modify code or settings. For production or money-related changes, require the applicable authorization and safe rollback strategy.

## 7 — Learn (never silently)
Capture a reusable lesson only when it has credible observations, applicability, exceptions and a repeatable verification method. Classify as **project-only**, **category**, **general candidate**, or **no rule change**. Run conflict/scope checks and propose a human-reviewed rule improvement. A one-off incident does not automatically become a global rule. Do not mix company-specific facts across employers or into the personal repository.

## Response shape (plain English, without showing a huge template)
1. **What I found:** confirmed observations.
2. **What I ruled out:** only alternatives with contradicting evidence.
3. **Conclusion:** confirmed / likely / unresolved and why.
4. **Next action:** minimal recommendation or exact missing check; distinguish code changed from diagnosis only.
5. **Lesson candidate:** only if reusable, sanitized and supported.

Do not substitute a pretty report for real investigation. If tools or access are missing, be explicit and explain what can be checked next. When code is changed, respect the project's commit and readable release-note instructions.

### Portable use
The compact, self-contained prompt for assistants that cannot access this repository is at [../../USE-ANYWHERE.md](../../USE-ANYWHERE.md). A connection to the repository or a pasted prompt is required to actually invoke its guidance in other tools; simply writing this skill cannot remotely control another agent.
